#!/bin/sh
# Condition B2 (servers/rover_schema_mcp.py) under a chosen Python, for Goose runs.
# Goose resolves the script's "#!/usr/bin/env python3" through PATH; on a machine where that
# is the python.org build without "Install Certificates", GitHub's TLS handshake fails, the
# agent returns the error text as its answer, and the run still exits 0.
# Set B2_PYTHON to a Python with a working trust store (default: .tools/bin/python3).
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec "${B2_PYTHON:-$ROOT/.tools/bin/python3}" "$ROOT/servers/rover_schema_mcp.py" "$@"
