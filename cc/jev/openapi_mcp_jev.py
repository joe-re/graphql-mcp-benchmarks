#!/usr/bin/env python3
"""M-R1's endpoint tools with Jev in front: `--gate` (M-R6) or `--prune` (M-R7).

  --gate   Expose only the tools named in $JEV_TOOLS (comma-separated operationIds).
           The runner picks them with Jev before the agent starts (cc/jev/run_bc.py).
  --prune  Expose all nine tools, but before a response is returned, ask Jev which of
           its leaf fields are needed to answer $JEV_REQUEST and drop the rest. Record
           links keep their `id` so the agent can still join. Decisions are cached per
           field path for the life of the server (one run). Every Jev call is logged
           to $JEV_LOG.

Everything else is servers/openapi_mcp.py, unchanged.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [os.path.join(ROOT, "servers"), HERE]

import openapi_mcp  # noqa: E402
import jev_client as jev  # noqa: E402

YES = 0.5
_decisions = {}


def _paths(node, prefix=""):
    if isinstance(node, list):
        out = []
        for item in node:
            out += _paths(item, prefix)
        return out
    if isinstance(node, dict):
        if set(node) == {"id", "href"}:
            return [f"{prefix}.id" if prefix else "id"]
        out = []
        for k, v in node.items():
            out += _paths(v, f"{prefix}.{k}" if prefix else k)
        return out
    return [prefix]


def _prune(node, keep, prefix=""):
    if isinstance(node, list):
        return [_prune(item, keep, prefix) for item in node]
    if isinstance(node, dict):
        if set(node) == {"id", "href"}:
            return {"id": node["id"]}
        out = {}
        for k, v in node.items():
            p = f"{prefix}.{k}" if prefix else k
            if any(x == p or x.startswith(p + ".") for x in keep):
                out[k] = _prune(v, keep, p)
        return out
    return node


def pruned_dispatch(catalog, name, args):
    raw = _original_dispatch(catalog, name, args)
    try:
        body = json.loads(raw)
    except ValueError:
        return raw
    if not isinstance(body, dict) or "data" not in body:
        return raw
    op = catalog.by_operation_id[name]
    paths = sorted(set(_paths(body["data"])))
    todo = [p for p in paths if (name, p) not in _decisions and p != "id" and not p.endswith(".id")]
    if todo:
        state = {"request": os.environ.get("JEV_REQUEST", "")}
        qs = {f"f{i}": jev.noul(
            {"endpoint": op["operationId"], "endpoint_description": op["summary"], "field": p,
             "question": "Is the value of `field` in the `endpoint` response needed to answer `request`?"},
            true="The answer states this value, the answer cannot be worked out without it, or it is needed to look up related records.",
            false="The answer can be produced without this value, even if it is related or would be nice context.")
            for i, p in enumerate(todo)}
        ans = jev.ask(state, qs, os.environ.get("JEV_LOG"), label=f"prune:{name}")["answers"]
        for i, p in enumerate(todo):
            _decisions[(name, p)] = ans[f"f{i}"]["noul"] > YES
    keep = {p for p in paths if p == "id" or p.endswith(".id") or _decisions.get((name, p))}
    out = {"data": _prune(body["data"], keep)}
    next_cursor = (body.get("meta") or {}).get("nextCursor")
    if next_cursor:
        out["meta"] = {"nextCursor": next_cursor}
    return json.dumps(out, separators=(",", ":"))


_original_dispatch = openapi_mcp.dispatch_endpoint_tool

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "--gate":
        allowed = {t for t in os.environ.get("JEV_TOOLS", "").split(",") if t}
        _init = openapi_mcp.Catalog.__init__

        def gated_init(self, *a, **kw):
            _init(self, *a, **kw)
            self.operations = [op for op in self.operations if op["operationId"] in allowed]
            self.by_operation_id = {op["operationId"]: op for op in self.operations}

        openapi_mcp.Catalog.__init__ = gated_init
    elif mode == "--prune":
        openapi_mcp.dispatch_endpoint_tool = pruned_dispatch
    else:
        sys.exit("usage: openapi_mcp_jev.py --gate | --prune")
    sys.argv = [sys.argv[0], "--mode", "tools"]
    openapi_mcp.main()
