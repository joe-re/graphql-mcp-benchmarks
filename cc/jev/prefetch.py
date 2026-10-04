"""Condition M-R5: Jev plans what to fetch, code fetches, joins and projects; no LLM tool use.

  plan(request)  Jev decides, from the request text and the OpenAPI documents alone:
                   - which batch parameter the identifiers in the request belong to (Choice)
                   - which resources are needed (one Noul each)
                   - which enum values of non-entry resources to keep (one Noul each)
                   - which leaf fields of each needed resource are needed (one Noul each)
                 Identifiers are pulled out of the request with a regex, because Jev does
                 not generate strings.
  fetch(plan)    Code walks the relations from the entry resource to every needed one,
                 calls the lean REST list endpoints in batches (with `fields=` for the
                 top-level names), joins by id, filters, and keeps only the chosen leaves.

Nothing here knows about any task. The only inputs are the request and the specs.
"""
import json
import re
import sys

import jev_client as jev
from catalog import Catalog, project, ref_id

YES = 0.5
ID_TOKEN = re.compile(r"\b(?=[A-Z0-9-]*\d)(?=[A-Z0-9-]*[A-Z])[A-Z0-9]+(?:-[A-Z0-9]+)*\b")


def _selectable(param):
    """Top-level names the lean `fields` parameter documents as selectable."""
    m = re.search(r"Selectable names:\s*(.+?)\.?$", (param or {}).get("description", ""))
    return {n.strip() for n in m.group(1).split(",")} if m else set()


def plan(request: str, cat: Catalog, log_path=None) -> dict:
    identifiers = list(dict.fromkeys(ID_TOKEN.findall(request)))
    id_params = {f"{r}.{p}": (res["params"][p].get("description") or p)
                 for r, res in cat.resources.items() for p in res["params"]
                 if "comma-separated" in (res["params"][p].get("description") or "").lower()
                 and p != "fields"}
    state = {"request": request}
    q = {"entry": jev.choice(
        {"identifiers": identifiers[:8],
         "question": "The request names the records in `identifiers`. Which API parameter takes these identifiers?"},
        id_params)}
    for r, res in cat.resources.items():
        q[f"need__{r}"] = jev.noul(
            {"resource": r, "resource_description": res["description"],
             "question": "Does answering `request` need any data from `resource`?"})
        for leaf in res["leaves"]:
            for value in leaf["enum"] or []:
                q[f"keep__{r}__{leaf['path']}__{value}"] = jev.noul(
                    {"resource": r, "field": leaf["path"], "value": value,
                     "question": "To answer `request`, are records of `resource` whose `field` equals `value` needed?"})
    first = jev.ask(state, q, log_path, label="plan:resources")["answers"]

    entry_res, entry_param = first["entry"]["choice"].split(".", 1)
    needed = {r for r in cat.resources if first[f"need__{r}"]["noul"] > YES} | {entry_res}
    keep = {}
    for key, ans in first.items():
        if key.startswith("keep__"):
            _, r, path, value = key.split("__", 3)
            keep.setdefault((r, path), {})[value] = ans["noul"] > YES

    fields = {}
    for r in sorted(needed):
        res = cat.resources[r]
        # Links between records ({id, href} fields) are followed by code, so they are
        # never a question: joining is not a judgement.
        ref_heads = set(res["refs"])
        candidates = [leaf for leaf in res["leaves"] if leaf["path"].split(".", 1)[0] not in ref_heads]
        fq = {f"f{i}": jev.noul(
            {"resource": r, "field": leaf["path"], "field_description": leaf["description"] or None,
             "question": "Is the value of `field` in `resource` needed to answer `request`?"},
            true="The answer states this value, or the answer cannot be worked out without it.",
            false="The answer can be produced without this value, even if it is related or would be nice context.")
            for i, leaf in enumerate(candidates)}
        ans = jev.ask(state, fq, log_path, label=f"plan:fields:{r}")["answers"]
        fields[r] = [leaf["path"] for i, leaf in enumerate(candidates) if ans[f"f{i}"]["noul"] > YES]

    filters = {f"{r}.{path}": sorted(v for v, ok in vals.items() if ok)
               for (r, path), vals in keep.items()
               if r != entry_res and r in needed and not all(vals.values()) and any(vals.values())}
    return {"identifiers": identifiers, "entry": {"resource": entry_res, "param": entry_param},
            "needed": sorted(needed), "fields": fields, "filters": filters}


def _route(cat, entry, targets):
    """Resources on the shortest relation paths from `entry` to every target."""
    prev, frontier, seen = {}, [entry], {entry}
    while frontier:
        nxt = []
        for src in frontier:
            for tgt, kind, key in cat.relations(src):
                if tgt not in seen:
                    seen.add(tgt)
                    prev[tgt] = (src, kind, key)
                    nxt.append(tgt)
        frontier = nxt
    edges = {}
    for t in targets:
        while t != entry and t in prev:
            edges[t] = prev[t]
            t = prev[t][0]
    return edges  # target -> (source, kind, key)


def fetch(p: dict, cat: Catalog) -> dict:
    entry = p["entry"]["resource"]
    edges = _route(cat, entry, [r for r in p["needed"] if r != entry])

    def rest_fields(r, extra):
        names = _selectable(cat.resources[r]["params"].get("fields"))
        top = {f.split(".", 1)[0] for f in p["fields"].get(r, [])} | set(extra)
        return ",".join(sorted(top & names)) if names else None

    join_keys = {r: set() for r in cat.resources}
    for tgt, (src, kind, key) in edges.items():
        if kind == "forward":
            join_keys[src].add(key)
        else:
            join_keys[tgt].add(key[1])

    records = {}
    params = {p["entry"]["param"]: ",".join(p["identifiers"])}
    f = rest_fields(entry, join_keys[entry] | {"id"})
    records[entry] = cat.list_records(entry, dict(params, **({"fields": f} if f else {})))

    order = sorted(edges, key=lambda t: _depth(edges, t))
    for tgt in order:
        src, kind, key = edges[tgt]
        f = rest_fields(tgt, join_keys[tgt] | {"id"})
        extra = {"fields": f} if f else {}
        if kind == "forward":
            ids = sorted({ref_id(r.get(key)) for r in records[src]} - {None})
            got = cat.list_records(tgt, dict({"ids": ",".join(ids)}, **extra)) if ids else []
            by_id = {r["id"]: r for r in got}
            for r in records[src]:
                r["__" + re.sub(r"Id$", "", key)] = by_id.get(ref_id(r.get(key)))
            records[tgt] = got
        else:
            param, ref_field = key
            got = cat.list_records(tgt, dict({param: ",".join(r["id"] for r in records[src])}, **extra))
            for flt, allowed in p["filters"].items():
                r_name, path = flt.split(".", 1)
                if r_name == tgt:
                    got = [g for g in got if g.get(path) in allowed]
            groups = {}
            for g in got:
                groups.setdefault(ref_id(g.get(ref_field)), []).append(g)
            for r in records[src]:
                r["__" + tgt] = groups.get(r["id"], [])
            records[tgt] = got

    def shape(r_name, rec):
        out = project(rec, sorted(set(p["fields"].get(r_name, [])) | ({"id"} if r_name == entry else set())))
        for tgt, (src, kind, key) in edges.items():
            if src != r_name:
                continue
            slot = "__" + (re.sub(r"Id$", "", key) if kind == "forward" else tgt)
            child = rec.get(slot)
            name = slot[2:]
            out[name] = [shape(tgt, c) for c in child] if isinstance(child, list) else (
                shape(tgt, child) if child else None)
        return out

    return {entry: [shape(entry, r) for r in records[entry]]}


def _depth(edges, t):
    d = 0
    while t in edges:
        t = edges[t][0]
        d += 1
    return d


if __name__ == "__main__":
    cat = Catalog()
    request = sys.stdin.read()
    pl = plan(request, cat, log_path=sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps(pl, indent=1))
    print(json.dumps(fetch(pl, cat))[:1500])
