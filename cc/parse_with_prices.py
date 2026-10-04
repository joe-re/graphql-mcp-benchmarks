"""parse_logs.py with prices for Sonnet 5 / Opus 5.5 / Fable 5.1 (see cc/models.py).

  RESULTS_DIR=<out> python3 cc/parse_with_prices.py <runs dir>
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cc"))

import grade  # noqa: E402
import models  # noqa: E402
import parse_logs  # noqa: E402

models.extend(parse_logs._PRICING)

# M-R4 (cc/bff/): M-R1 plus a BFF endpoint with expand/fields. Registered here so a
# runs tree containing it parses instead of being refused as an unknown condition.
if "M-R4" not in parse_logs.PHASE_CONDS[2]:
    parse_logs.PHASE_CONDS[2].insert(parse_logs.PHASE_CONDS[2].index("M-R3") + 1, "M-R4")
    parse_logs.COND_PHASE["M-R4"] = 2
    parse_logs.MCP_CONDS.append("M-R4")
    parse_logs.COND_LABEL["M-R4"] = "REST (one tool per endpoint + BFF expand/fields)"
    parse_logs.COND_SHORT["M-R4"] = "M-R4\nREST + BFF expand"
for _cond, _label in (("M-R6", "REST (Jev picks which endpoint tools to expose)"),
                      ("M-R7", "REST (Jev prunes every response)"),
                      ("M-R8", "REST (Jev plan + code fetch as one tool)")):
    if _cond not in parse_logs.PHASE_CONDS[2]:
        parse_logs.PHASE_CONDS[2].append(_cond)
        parse_logs.COND_PHASE[_cond] = 2
        parse_logs.MCP_CONDS.append(_cond)
        parse_logs.COND_LABEL[_cond] = _label
        parse_logs.COND_SHORT[_cond] = f"{_cond}\n{_label}"

# The phase-2 lede compares cells across the full six-condition matrix (M-G1 vs M-G2,
# fat vs lean) and raises on a subset run such as M-R1 + M-G2 only. The tables and
# CSVs do not depend on it, so a subset run skips the lede instead of failing.
_key_findings_phase2 = parse_logs._key_findings_phase2


def _key_findings_phase2_or_skip(rows, cells, tasks):
    try:
        return _key_findings_phase2(rows, cells, tasks)
    except (TypeError, KeyError, ValueError, ZeroDivisionError):
        return ["_Key findings skipped: this run covers a subset of the phase-2 matrix._"]


parse_logs._key_findings_phase2 = _key_findings_phase2_or_skip

# Claude Code appends a context-budget notice to every tool result it hands the model:
#   <system-reminder>\n<total_tokens>N tokens left</total_tokens>\n</system-reminder>
# The model really reads it, so it stays in the token counts, but it makes the result
# invalid JSON, and grade.pass_through_tokens then scores the whole result as unused.
# Strip it from the sidecar before grading. Goose runs never contain it.
_REMINDER = re.compile(r"\s*<system-reminder>\s*<total_tokens>[^<]*</total_tokens>\s*</system-reminder>\s*$")
_read_tool_io = grade.read_tool_io


def read_tool_io_stripped(path):
    calls = _read_tool_io(path)
    for call in calls:
        for res in call.get("tool_result") or []:
            if isinstance(res.get("content"), str):
                res["content"] = _REMINDER.sub("", res["content"])
    return calls


grade.read_tool_io = read_tool_io_stripped

if __name__ == "__main__":
    parse_logs.main()
