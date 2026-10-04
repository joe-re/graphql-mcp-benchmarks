"""Stand-in for `goose run --recipe <path> --no-session --max-turns N`, backed by `claude -p`.

run_benchmark.py launches this in place of Goose (see cc/run_cc.py), so the proxy,
the per-run directory layout, meta.json, the timeout and the budget kill are all the
upstream runner's own code. This file only translates one rendered Goose recipe into
one Claude Code invocation:

  recipe `instructions`  -> --system-prompt   (replaces Claude Code's default prompt)
  recipe `prompt`        -> the -p prompt
  recipe `extensions`    -> --mcp-config + --strict-mcp-config (only these servers)
  settings.goose_model   -> --model
  ANTHROPIC_HOST         -> ANTHROPIC_BASE_URL (the logging proxy, as for Goose)

Built-in tools are removed (`--tools ""`), thinking is off (MAX_THINKING_TOKENS=0)
and settings/CLAUDE.md sources are not loaded, so the agent holds only the
condition's MCP tools, as it does under Goose.

stdout is what run_benchmark.py saves as stdout.txt and what parse_logs.py's
stop_cause() reads: the final answer text, plus Goose's turn-cap phrase when Claude
Code stops on --max-turns, so a capped run is still classified as `turn cap`.
The raw stream-json goes to stream.jsonl beside the recipe.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

RELAY = Path(__file__).resolve().parent / "mcp_meta_relay.py"


def main() -> int:
    args = sys.argv[1:]
    recipe_path = Path(args[args.index("--recipe") + 1])
    max_turns = args[args.index("--max-turns") + 1] if "--max-turns" in args else "50"
    run_dir = recipe_path.parent
    recipe = yaml.safe_load(recipe_path.read_text())

    servers = {}
    for ext in recipe.get("extensions") or []:
        if ext.get("type") != "stdio":
            sys.exit(f"claude_shim: unsupported extension type {ext.get('type')!r}")
        # Env values are inherited from this process rather than written into the
        # config file, so the GitHub token never lands on disk. Every server runs
        # behind cc/mcp_meta_relay.py, which lifts Claude Code's 50,000-character
        # per-result limit so large payloads reach the model whole, as under Goose.
        servers[ext["name"]] = {"type": "stdio", "command": sys.executable,
                                "args": [str(RELAY), "--", str(ext["cmd"]),
                                         *[str(a) for a in ext.get("args") or []]]}
    mcp_config = run_dir / "mcp_config.json"
    mcp_config.write_text(json.dumps({"mcpServers": servers}, indent=2))

    model = (recipe.get("settings") or {}).get("goose_model") or "claude-haiku-4-5"
    cmd = [
        "claude", "-p", recipe["prompt"].strip(),
        "--model", model,
        "--system-prompt", recipe["instructions"].strip(),
        "--tools", "",
        "--mcp-config", str(mcp_config), "--strict-mcp-config",
        "--allowedTools", *[f"mcp__{name}" for name in servers],
        "--setting-sources", "",
        "--no-session-persistence",
        "--max-turns", str(max_turns),
        "--output-format", "stream-json", "--verbose",
    ]
    (run_dir / "claude_cmd.json").write_text(json.dumps(cmd, indent=2))

    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)          # subscription auth, not an API key
    env["ANTHROPIC_BASE_URL"] = env.get("ANTHROPIC_HOST", "https://api.anthropic.com")
    env["MAX_THINKING_TOKENS"] = "0"
    # Claude Code's MCP output token cap (25,000 by default) truncates results; the
    # relay above handles the separate 50,000-character persistence limit.
    env["MAX_MCP_OUTPUT_TOKENS"] = "200000"
    env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"

    # An empty working directory, so no project files or CLAUDE.md enter the context.
    with tempfile.TemporaryDirectory(prefix="cc-run-") as cwd:
        proc = subprocess.run(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                              capture_output=True, text=True)
    (run_dir / "stream.jsonl").write_text(proc.stdout)
    sys.stderr.write(proc.stderr)

    result = None
    for line in proc.stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            result = ev
    if result is None:
        print("claude_shim: no result event in stream-json output")
        return proc.returncode or 1
    text = result.get("result") or ""
    if result.get("subtype") == "error_max_turns":
        text += f"\n\n[claude_shim] reached the maximum number of actions ({max_turns} turns)"
    print(text)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
