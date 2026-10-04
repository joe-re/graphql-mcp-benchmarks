"""What the OpenAPI documents say, in the shape the Jev experiments need.

Everything here is derived mechanically from services/generated/*/openapi.json; there
is no per-task or per-field knowledge in this file.

  resources  one per batchable list endpoint (GET /v2/<name> whose 200 body is a list of
             a component schema): flights, aircraft, crew, assignments
  leaves     every scalar path in a resource's component schema ("model.code",
             "typeRatings.expiresAt"), with its description and enum
  relations  forward: a field named `<x>Id` whose schema is {id, href} points at the
             resource whose path starts with <x> ("aircraftId" -> aircraft)
             reverse: a list parameter named `<x>Ids` on another resource
             ("flightIds" on assignments -> assignments of each flight)
"""
import json
import os
import re
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC_DIR = os.path.join(ROOT, "services", "generated")
SERVICES = ("scheduling", "fleet", "personnel")
PAGE = 200


def _deref(schema, spec):
    while "$ref" in schema:
        schema = spec["components"]["schemas"][schema["$ref"].split("/")[-1]]
    return schema


def _is_ref(schema):
    props = schema.get("properties") or {}
    return schema.get("type") == "object" and set(props) == {"id", "href"}


def leaves(schema, spec, prefix=""):
    schema = _deref(schema, spec)
    if schema.get("type") == "object" and schema.get("properties"):
        out = []
        for key, sub in schema["properties"].items():
            out += leaves(sub, spec, f"{prefix}.{key}" if prefix else key)
        return out
    if schema.get("type") == "array":
        return leaves(schema.get("items") or {}, spec, prefix)
    return [{"path": prefix, "description": schema.get("description", ""), "enum": schema.get("enum")}]


class Catalog:
    def __init__(self):
        self.resources = {}
        for svc in SERVICES:
            spec = json.load(open(os.path.join(SPEC_DIR, svc, "openapi.json")))
            base = spec["servers"][0]["url"].rstrip("/")
            for path, methods in spec["paths"].items():
                op = methods.get("get")
                if not op or "{" in path:
                    continue
                body = op["responses"]["200"]["content"]["application/json"]["schema"]
                items = (body.get("properties") or {}).get("data", {}).get("items")
                if not items or "$ref" not in items:
                    continue
                schema_name = items["$ref"].split("/")[-1]
                schema = spec["components"]["schemas"][schema_name]
                name = path.rsplit("/", 1)[-1]
                self.resources[name] = {
                    "name": name, "service": svc, "base": base, "path": path,
                    "operationId": op["operationId"], "schema": schema_name,
                    "description": (op.get("summary", "") + ". " + op.get("description", "")).strip(),
                    "params": {p["name"]: p for p in op.get("parameters", [])},
                    "leaves": leaves(schema, spec),
                    "refs": {k: v.get("description", "") for k, v in (schema.get("properties") or {}).items()
                             if _is_ref(_deref(v, spec))},
                }

    def resource_for_ref(self, field):
        """`aircraftId` -> aircraft, `crewId` -> crew, `flightId` -> flights."""
        stem = re.sub(r"Id$", "", field).lower()
        return next((r for r in self.resources if r.lower().startswith(stem)), None)

    def relations(self, source):
        """(target, kind, key): forward via a ref field on `source`, or reverse via `<source>Ids`."""
        out = []
        for field in self.resources[source]["refs"]:
            target = self.resource_for_ref(field)
            if target and target != source:
                out.append((target, "forward", field))
        singular = re.sub(r"s$", "", source)
        for target, res in self.resources.items():
            param = f"{singular}Ids"
            if target != source and param in res["params"]:
                ref_field = f"{singular}Id"
                out.append((target, "reverse", (param, ref_field)))
        return out

    def list_records(self, resource, params):
        """Every page of a list endpoint. The payload never reaches a model, only code."""
        res = self.resources[resource]
        out, cursor = [], None
        while True:
            query = dict(params, limit=PAGE, **({"cursor": cursor} if cursor else {}))
            url = f"{res['base']}{res['path']}?{urllib.parse.urlencode(query)}"
            with urllib.request.urlopen(url, timeout=30) as resp:
                body = json.load(resp)
            out.extend(body.get("data") or [])
            cursor = (body.get("meta") or {}).get("nextCursor")
            if not cursor:
                return out


def ref_id(value):
    return value.get("id") if isinstance(value, dict) else value


def project(node, paths):
    """Keep only the dotted leaf `paths` of `node`; a path into a list applies per item."""
    if isinstance(node, list):
        return [project(item, paths) for item in node]
    if not isinstance(node, dict):
        return node
    heads = {}
    for p in paths:
        head, _, rest = p.partition(".")
        heads.setdefault(head, []).append(rest)
    out = {}
    for head, rests in heads.items():
        if head in node:
            v = node[head]
            out[head] = v if any(r == "" for r in rests) else project(v, [r for r in rests if r])
    return out
