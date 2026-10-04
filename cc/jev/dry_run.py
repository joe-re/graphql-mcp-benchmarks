# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Plan and fetch for a few tasks without any LLM call; prints what Jev chose and the data size."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "cc" / "jev")]
import run_benchmark as rb
from catalog import Catalog
import prefetch
tasks = {t["id"]: t for t in rb.load_tasks()}
cat = Catalog()
out = ROOT / "runs-cc" / "jev-dry"; out.mkdir(parents=True, exist_ok=True)
for tid in sys.argv[1:]:
    log = out / f"{tid}.jsonl"; log.write_text("")
    pl = prefetch.plan(tasks[tid]["prompt_rendered"], cat, str(log))
    data = prefetch.fetch(pl, cat); s = json.dumps(data, separators=(",", ":"))
    (out / f"{tid}.data.json").write_text(s); (out / f"{tid}.plan.json").write_text(json.dumps(pl, indent=1))
    jl = [json.loads(l) for l in log.read_text().splitlines()]
    print("=====", tid, "| entry", pl["entry"], "| needed", pl["needed"], "| filters", pl["filters"])
    for r, f in pl["fields"].items(): print("  ", r, f)
    print("   data bytes", len(s), "| jev calls", len(jl), "| jev input tokens", sum(x["usage"]["input_tokens"] for x in jl),
          "| cost $%.5f" % sum(x["cost_usd"] for x in jl))
    print("  ", s[:350])
