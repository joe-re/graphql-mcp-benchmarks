# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""run_benchmark.py with Goose, for models that reject sampling parameters.

Sonnet 5, Opus 5.5 and Fable 5.1 return `400: temperature is deprecated for this
model` on every request, and every upstream recipe sets `temperature: 0`. This drops
that one line from each rendered recipe and adds the models' prices; everything else
is the upstream runner, unmodified. Runs therefore use the model's default sampling,
which upstream's published Haiku 4.5 numbers did not.

  PROJECT_ROOT=$PWD RUNS_DIR=$PWD/runs-models/<model>/phase1 MODEL=<model> \
    uv run cc/run_goose_nosampling.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cc"))

import models  # noqa: E402
import run_benchmark as rb  # noqa: E402

_TEMPERATURE = re.compile(r"^\s*temperature:.*$")
_render_recipe = rb.render_recipe


def render_recipe(template_text: str, task_prompt: str, tokens: dict) -> str:
    text = _render_recipe(template_text, task_prompt, tokens)
    return "\n".join(l for l in text.splitlines() if not _TEMPERATURE.match(l)) + "\n"


rb.render_recipe = render_recipe
models.extend(rb._RUN_PRICING)

if __name__ == "__main__":
    rb.main()
