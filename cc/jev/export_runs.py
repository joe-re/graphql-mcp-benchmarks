"""Copy the per-run numbers that cc/jev/summarize.py needs out of runs-cc/ into results-cc/jev/.

  python3 cc/jev/export_runs.py

runs-cc/ holds the raw logs and is not committed (like upstream's runs/). M-R5 never goes
through parse_logs.py, and the Jev cost of M-R6/7/8 is only in each run's jev.jsonl, so
these two CSVs carry them into the committed results:

  results-cc/jev/m_r5.csv     one row per M-R5 run (from result.json)
  results-cc/jev/jev_cost.csv one row per M-R6/7/8 run (sum of jev.jsonl cost_usd)
"""
import csv
import glob
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "runs-cc" / "jev"
OUT = ROOT / "results-cc" / "jev"
USAGE = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")


def main():
    rows = []
    for f in sorted(glob.glob(str(RUNS / "M-R5-lean/*/*/rep*/result.json"))):
        p = Path(f)
        r = json.loads(p.read_text())
        rows.append({"model": p.parts[-4], "task_id": p.parts[-3], "rep": p.parts[-2].removeprefix("rep"),
                     "claude_inference_calls": r["claude_inference_calls"],
                     **{k: r["claude_usage"][k] for k in USAGE},
                     "data_tokens_cl100k": r["data_tokens_cl100k"], "answer_f1": r["answer_f1"],
                     "jev_cost_usd": r["jev_cost_usd"]})
    write(OUT / "m_r5.csv", rows)

    rows = []
    for f in sorted(glob.glob(str(RUNS / "*/M-R[678]-lean/*/rep*/jev.jsonl"))):
        p = Path(f)
        cost = sum(json.loads(l)["cost_usd"] for l in p.read_text().splitlines() if l.strip())
        rows.append({"model": p.parts[-5], "cell": p.parts[-4], "task_id": p.parts[-3],
                     "rep": p.parts[-2].removeprefix("rep"), "jev_cost_usd": cost})
    write(OUT / "jev_cost.csv", rows)


def write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"{path.relative_to(ROOT)}: {len(rows)} rows")


if __name__ == "__main__":
    main()
