# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Run conditions M-R6 (Jev picks the tools) and M-R7 (Jev prunes responses) with claude -p.

  RUNS_DIR=runs-cc/jev MODEL=claude-sonnet-5 PAYLOAD_PROFILE=lean \
    uv run cc/jev/run_bc.py M-R6:M3@20:1 M-R7:M3@20:1

M-R6: before the agent starts, one Jev call asks, for each of M-R1's nine tools, whether
the request needs it (Noul). Only the tools above 0.5 are exposed ($JEV_TOOLS).
M-R7: the agent sees all nine tools; the MCP server prunes each response with Jev
($JEV_REQUEST, logged to $JEV_LOG in the run directory).
Otherwise both are the upstream runner, via cc/rerun_cc.py.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CC = HERE.parent
sys.path[:0] = [str(CC), str(HERE), str(CC.parent / "servers")]

import rerun_cc  # noqa: E402  (imports run_cc, which patches run_benchmark for claude -p)
import jev_client as jev  # noqa: E402
import openapi_mcp  # noqa: E402

rb = rerun_cc.rb
for cond in ("M-R6", "M-R7", "M-R8"):
    rb.CONDITIONS[cond] = (str(CC / "recipes" / f"recipe_{cond.lower().replace('-', '_')}.yaml"),
                           {"phase": 2, "surface": "rest", "profiles": ("fat", "lean")})

_render_recipe = rb.render_recipe


def render_recipe(template_text, task_prompt, tokens):
    tokens = dict(tokens, **{"@@OPENAPI_MCP_JEV@@": str(HERE / "openapi_mcp_jev.py"),
                             "@@JEV_FETCH_MCP@@": str(HERE / "mcp_jev_fetch.py")})
    return _render_recipe(template_text, task_prompt, tokens)


rb.render_recipe = render_recipe


def pick_tools(request: str, log_path: str) -> list:
    tools = openapi_mcp.build_endpoint_tools(openapi_mcp.Catalog(openapi_mcp.DEFAULT_SPEC_DIR, {}))
    qs = {f"t{i}": jev.noul(
        {"tool": t["name"], "tool_description": t["description"],
         "question": "Could `tool` be needed to answer `request`?"},
        true="Answering the request may require data this tool returns.",
        false="This tool returns nothing the request asks about or depends on.")
        for i, t in enumerate(tools)}
    ans = jev.ask({"request": request}, qs, log_path, label="gate:tools")["answers"]
    return [t["name"] for i, t in enumerate(tools) if ans[f"t{i}"]["noul"] > 0.5]


def main(specs):
    tasks = {t["id"]: t for t in rb.load_tasks()}
    for spec in specs:
        cond, task_id, rep = spec.split(":")
        cond_dir = f"{cond}-{rb.PAYLOAD_PROFILE}"
        run_dir = rb.RUNS_DIR / cond_dir / task_id / f"rep{rep}"
        run_dir.mkdir(parents=True, exist_ok=True)
        jev_log = run_dir / "jev.jsonl"
        jev_log.write_text("")
        request = tasks[task_id]["prompt_rendered"]
        os.environ["JEV_REQUEST"] = request
        os.environ["JEV_LOG"] = str(jev_log)
        if cond == "M-R6":
            chosen = pick_tools(request, str(jev_log))
            os.environ["JEV_TOOLS"] = ",".join(chosen)
            (run_dir / "jev_tools.json").write_text(json.dumps(chosen))
            print(f"  Jev picked {len(chosen)} tool(s): {', '.join(chosen)}", flush=True)
        rerun_cc.main([spec])


if __name__ == "__main__":
    main(sys.argv[1:])
