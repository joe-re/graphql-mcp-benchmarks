"""stdio relay between Claude Code and one MCP server: `mcp_meta_relay.py -- <cmd> [args...]`.

Claude Code persists any tool result above 50,000 characters to a file and hands the
model a 2 KB preview instead ("Output too large ... Preview (first 2KB)"). Goose
passes results through whole, so under Claude Code the large REST payloads the
benchmark exists to measure were silently clipped. A server can raise the limit per
tool (up to 500,000 characters) with the `anthropic/maxResultSizeChars` key in the
tool's `_meta`; this relay adds that key to every tool in each `tools/list` response
and forwards everything else byte-for-byte. `_meta` is read by the client and is not
sent to the model, so the tool surface the model sees is unchanged.
"""
import json
import subprocess
import sys
import threading

MAX_RESULT_SIZE_CHARS = 500_000


def main() -> int:
    argv = sys.argv[1:]
    if argv and argv[0] == "--":
        argv = argv[1:]
    proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def client_to_server():
        for line in sys.stdin.buffer:
            proc.stdin.write(line)
            proc.stdin.flush()
        proc.stdin.close()

    threading.Thread(target=client_to_server, daemon=True).start()

    out = sys.stdout.buffer
    for line in proc.stdout:
        try:
            msg = json.loads(line)
        except ValueError:
            out.write(line)
            out.flush()
            continue
        tools = (msg.get("result") or {}).get("tools") if isinstance(msg, dict) else None
        if isinstance(tools, list):
            for tool in tools:
                tool.setdefault("_meta", {})["anthropic/maxResultSizeChars"] = MAX_RESULT_SIZE_CHARS
            line = (json.dumps(msg) + "\n").encode()
        out.write(line)
        out.flush()
    return proc.wait()


if __name__ == "__main__":
    sys.exit(main())
