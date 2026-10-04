#!/usr/bin/env python3
"""M-R4: M-R1's nine endpoint tools plus the BFF's `listFlightExpanded`, as one MCP server.

Runs servers/openapi_mcp.py unchanged in `--mode tools`, with a fourth service
(`gateway`, cc/bff/bff_server.py on :4004) added to its service list and a spec
directory that links the three generated service specs next to the gateway's. The
tool is generated from the gateway's OpenAPI document by the same code that makes
M-R1's nine, so the only thing that differs from M-R1 is the extra endpoint.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "servers"))

import openapi_mcp  # noqa: E402

openapi_mcp.SERVICES = ("scheduling", "fleet", "personnel", "gateway")

if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--mode", "tools", "--spec-dir", os.path.join(HERE, "spec"), *sys.argv[1:]]
    openapi_mcp.main()
