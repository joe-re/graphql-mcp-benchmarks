#!/usr/bin/env python3
"""A REST BFF with OData-style `expand` and `fields`, in front of the three phase-2 services.

    GET /v2/flights?ids=FL-0001,FL-0002
                   &expand=aircraft,assignments.crew
                   &fields=id,aircraft.model.code,assignments.role,assignments.crew.typeRatings.expiresAt
                   &assignmentRoles=CAPTAIN,FIRST_OFFICER

One request follows the flight -> aircraft and flight -> assignments -> crew links
server-side and returns only the requested paths, which is what the GraphQL router
does for M-G3. It exists to test one claim: that the gap between REST and GraphQL in
M3 comes from whether a single call can express the traversal and the projection,
not from the protocol or from how many services sit behind it.

The backends are the unmodified scheduling / fleet / personnel REST services. They are
called without `fields`, so the projection here does not depend on their payload
profile. Standard library only.

  python3 cc/bff/bff_server.py [--port 4004]
"""
import argparse
import json
import os
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BACKENDS = {
    "scheduling": os.environ.get("BENCH_SCHEDULING_URL", "http://localhost:4001"),
    "fleet": os.environ.get("BENCH_FLEET_URL", "http://localhost:4002"),
    "personnel": os.environ.get("BENCH_PERSONNEL_URL", "http://localhost:4003"),
}
EXPANDABLE = {"aircraft", "assignments", "assignments.crew"}
MAX_IDS = 100
PAGE = 200
API_VERSION = "2024-11-01"


class BadRequest(Exception):
    pass


def _csv(value):
    return [v.strip() for v in (value or "").split(",") if v.strip()]


def _ref_id(value):
    """A link field is `{"id": ..., "href": ...}` in these payloads; accept a bare id too."""
    return value.get("id") if isinstance(value, dict) else value


def _list(service, path, params):
    """Every page of a backend list endpoint."""
    out, cursor = [], None
    while True:
        query = dict(params, limit=PAGE, **({"cursor": cursor} if cursor else {}))
        url = f"{BACKENDS[service]}{path}?{urllib.parse.urlencode(query)}"
        with urllib.request.urlopen(url, timeout=30) as resp:
            body = json.load(resp)
        out.extend(body.get("data") or [])
        cursor = (body.get("meta") or {}).get("nextCursor")
        if not cursor:
            return out


def _project(node, paths):
    """Keep only the dotted `paths` (relative to `node`); lists apply the path per item."""
    if isinstance(node, list):
        return [_project(item, paths) for item in node]
    if not isinstance(node, dict):
        return node
    heads = {}
    for p in paths:
        head, _, rest = p.partition(".")
        heads.setdefault(head, []).append(rest)
    out = {}
    for head, rests in heads.items():
        if head not in node:
            continue
        value = node[head]
        out[head] = value if any(r == "" for r in rests) else _project(value, [r for r in rests if r])
    return out


def expanded_flights(query):
    ids = _csv(query.get("ids"))
    if not ids:
        raise BadRequest("`ids` is required: comma-separated flight ids")
    if len(ids) > MAX_IDS:
        raise BadRequest(f"at most {MAX_IDS} ids per request")
    expand = set(_csv(query.get("expand")))
    unknown = expand - EXPANDABLE
    if unknown:
        raise BadRequest(f"unknown expand path(s): {', '.join(sorted(unknown))}; "
                         f"expandable: {', '.join(sorted(EXPANDABLE))}")
    if "assignments.crew" in expand:
        expand.add("assignments")
    roles = set(_csv(query.get("assignmentRoles")))
    fields = _csv(query.get("fields"))

    flights = _list("scheduling", "/v2/flights", {"ids": ",".join(ids)})

    if "aircraft" in expand:
        aircraft_ids = sorted({_ref_id(f.get("aircraftId")) for f in flights} - {None})
        aircraft = {a["id"]: a for a in _list("fleet", "/v2/aircraft", {"ids": ",".join(aircraft_ids)})}
        for f in flights:
            f["aircraft"] = aircraft.get(_ref_id(f.get("aircraftId")))

    if "assignments" in expand:
        assignments = _list("personnel", "/v2/assignments", {"flightIds": ",".join(f["id"] for f in flights)})
        if roles:
            assignments = [a for a in assignments if a.get("role") in roles]
        if "assignments.crew" in expand:
            crew_ids = sorted({_ref_id(a.get("crewId")) for a in assignments} - {None})
            crew = {c["id"]: c for c in _list("personnel", "/v2/crew", {"ids": ",".join(crew_ids)})}
            for a in assignments:
                a["crew"] = crew.get(_ref_id(a.get("crewId")))
        by_flight = {}
        for a in assignments:
            by_flight.setdefault(_ref_id(a.get("flightId")), []).append(a)
        for f in flights:
            f["assignments"] = by_flight.get(f["id"], [])

    data = [_project(f, ["id", *fields]) for f in flights] if fields else flights
    return {"meta": {"apiVersion": API_VERSION, "count": len(data), "expand": sorted(expand)},
            "data": data}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body):
        payload = json.dumps(body, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        query = {k: v[-1] for k, v in urllib.parse.parse_qs(url.query).items()}
        try:
            if url.path == "/__health":
                return self._send(200, {"ok": True})
            if url.path == "/v2/flights":
                return self._send(200, expanded_flights(query))
            return self._send(404, {"error": f"no route for {url.path}"})
        except BadRequest as e:
            return self._send(400, {"error": str(e)})
        except Exception as e:  # a backend being down should read as an error, not a hang
            return self._send(502, {"error": f"backend request failed: {e}"})

    def log_message(self, fmt, *args):
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=4004)
    args = ap.parse_args()
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
