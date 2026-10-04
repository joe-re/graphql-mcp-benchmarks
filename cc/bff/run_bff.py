# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Run specific M-R4 (REST + BFF expand/fields) runs with claude -p.

Registers condition M-R4 with the upstream runner (recipe cc/recipes/recipe_m_r4.yaml,
server cc/bff/openapi_mcp_bff.py), then hands the listed runs to cc/rerun_cc.py. The
BFF itself (cc/bff/bff_server.py) must already be listening on :4004.

  RUNS_DIR=... MODEL=... PAYLOAD_PROFILE=lean uv run cc/bff/run_bff.py M-R4:M3@20:1
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CC = HERE.parent
sys.path.insert(0, str(CC))

import rerun_cc  # noqa: E402  (imports run_cc, which patches run_benchmark for claude -p)

rb = rerun_cc.rb
rb.CONDITIONS["M-R4"] = (str(CC / "recipes" / "recipe_m_r4.yaml"),
                         {"phase": 2, "surface": "rest", "profiles": ("fat", "lean")})

_render_recipe = rb.render_recipe


def render_recipe(template_text, task_prompt, tokens):
    tokens = dict(tokens, **{"@@OPENAPI_MCP_BFF@@": str(HERE / "openapi_mcp_bff.py")})
    return _render_recipe(template_text, task_prompt, tokens)


rb.render_recipe = render_recipe

if __name__ == "__main__":
    rerun_cc.main(sys.argv[1:])
