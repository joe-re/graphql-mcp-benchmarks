#!/usr/bin/env python3
"""M-R8: condition M-R5's Jev plan + code fetch, exposed as one MCP tool.

    fetch_airline_data(question)

The agent writes what it needs, including the record identifiers. Jev plans from that
question (cc/jev/prefetch.py: entry parameter, resources, enum filters, leaf fields),
code fetches from the lean REST services, joins and projects, and the tool returns the
records plus a short `returned_fields` summary so the agent can see what it got and ask
again if something is missing. Every Jev call is logged to $JEV_LOG.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [os.path.join(ROOT, "servers"), HERE]

from _mcp_stdio import make_logger, serve  # noqa: E402
from catalog import Catalog  # noqa: E402
import prefetch  # noqa: E402

_log = make_logger("jev-fetch")
TOOL = {
    "name": "fetch_airline_data",
    "description": (
        "Fetch records from the airline's operational systems (flights, aircraft, crew assignments, "
        "crew members) in one call. Describe in plain English what information you need and include "
        "every record identifier from the request. The records are joined across services and "
        "reduced to the fields judged necessary for your question; `returned_fields` lists them."),
    "inputSchema": {
        "type": "object",
        "properties": {"question": {
            "type": "string",
            "description": "What you need to know, including the identifiers (flight ids, flight numbers, ...)."}},
        "required": ["question"],
    },
}


def main():
    cat = Catalog()

    def dispatch(name, args):
        if name != TOOL["name"]:
            raise ValueError(f"unknown tool: {name}")
        question = (args or {}).get("question") or ""
        plan = prefetch.plan(question, cat, os.environ.get("JEV_LOG"))
        if not plan["identifiers"]:
            return json.dumps({"error": "no record identifiers found in `question`; include them"})
        data = prefetch.fetch(plan, cat)
        data["returned_fields"] = plan["fields"]
        return json.dumps(data, separators=(",", ":"))

    serve(name="jev-fetch", version="0.1.0", tools=[TOOL], dispatch=dispatch, log=_log)


if __name__ == "__main__":
    main()
