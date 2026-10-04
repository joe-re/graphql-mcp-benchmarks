# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Re-run specific (condition, task, rep) runs with claude -p, in place.

The upstream runner only knows "REPS=N for every selected task", so re-running
one failed rep means re-running its siblings too. This calls the same run_one()
for exactly the listed runs, into the same RUNS_DIR, so they replace the failed
ones and parse alongside the rest.

  RUNS_DIR=$PWD/runs-cc/phase2/<model> MODEL=<model> PAYLOAD_PROFILE=fat \
    uv run cc/rerun_cc.py M-R1:M1@50:3 M-G2:M3@5:1 ...
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_cc  # noqa: E402  (applies the claude -p patches to run_benchmark)

rb = run_cc.rb


def main(specs: list) -> None:
    tasks = {t["id"]: t for t in rb.load_tasks()}
    runs = []
    for spec in specs:
        cond, task_id, rep = spec.split(":")
        if cond not in rb.CONDITIONS or task_id not in tasks:
            sys.exit(f"unknown run {spec!r}")
        runs.append((cond, tasks[task_id], int(rep)))
    rb.services_up(sorted({c for c, _, _ in runs}))
    base_env = dict(os.environ)
    base_env["PATH"] = f"{rb.ROOT / 'bin'}{os.pathsep}{base_env.get('PATH', '')}"
    for cond, task, rep in runs:
        rb.run_one(cond, task, rep, base_env, port=rb.PORT)


if __name__ == "__main__":
    main(sys.argv[1:])
