"""Phase-2 M1/M3 comparison across models: claude -p runs vs the published Haiku runs.

  python3 cc/compare_phase2.py            # prints Markdown tables

Reads results-cc/phase2/<model>/raw.csv (written by cc/parse_with_prices.py) and the
committed results/phase2/raw.csv. Cost is recomputed from token counts with each
model's price; claude -p writes every cache entry with the 1-hour TTL (2x input),
so its cache writes are priced at 2x rather than parse_logs' 5-minute 1.25x.
"""
import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cc"))

import models  # noqa: E402
import parse_logs  # noqa: E402

models.extend(parse_logs._PRICING)

MODELS = ["claude-haiku-4-5", "claude-sonnet-5", "claude-opus-5-5", "claude-fable-5-1"]
CELLS = ["M-R1-fat", "M-G2"]
TASKS = ["M1@1", "M1@5", "M1@20", "M1@50", "M3@5", "M3@20", "M3@50"]


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def cost(row, model, cache_write_mult):
    p = parse_logs._price_for(model)
    get = lambda k: num(row.get(k)) or 0.0
    return (get("proxy_input_tokens") * p["input"]
            + get("proxy_output_tokens") * p["output"]
            + get("proxy_cache_read_input_tokens") * p["cache_read"]
            + get("proxy_cache_creation_input_tokens") * p["input"] * cache_write_mult) / 1e6


def load(path, model, cache_write_mult):
    out = defaultdict(list)
    for r in csv.DictReader(open(path)):
        if r["cell"] in CELLS and r["task_id"] in TASKS:
            r["_cost"] = cost(r, model, cache_write_mult)
            out[(r["cell"], r["task_id"])].append(r)
    return out


def mean(rows, key):
    vals = [num(r[key]) if key != "_cost" else r["_cost"] for r in rows]
    vals = [v for v in vals if v is not None]
    return statistics.mean(vals) if vals else None


def fmt(v, spec):
    return "—" if v is None else format(v, spec)


def main():
    sources = {"published (Goose, haiku-4-5)": load(ROOT / "results/phase2/raw.csv",
                                                    "claude-haiku-4-5", 1.25)}
    for m in MODELS:
        path = ROOT / "results-cc/phase2" / m / "raw.csv"
        if path.exists():
            sources[f"claude -p, {m.removeprefix('claude-')}"] = load(path, m, 2.0)

    print("| source | task | REST pass-through | GraphQL pass-through | ratio | "
          "REST $/run | GraphQL $/run | cost ratio | REST f1 | GraphQL f1 | incomplete |")
    print("|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    for name, data in sources.items():
        for t in TASKS:
            rest, gql = data.get(("M-R1-fat", t), []), data.get(("M-G2", t), [])
            if not rest and not gql:
                continue
            rp, gp = mean(rest, "pass_through_tokens"), mean(gql, "pass_through_tokens")
            rc, gc = mean(rest, "_cost"), mean(gql, "_cost")
            incomplete = sum(1 for r in rest + gql if r.get("completed") not in ("True", "true", "1"))
            print(f"| {name} | {t} | {fmt(rp, ',.0f')} | {fmt(gp, ',.0f')} | "
                  f"{fmt(rp / gp if rp and gp else None, '.1f')}x | {fmt(rc, '.4f')} | {fmt(gc, '.4f')} | "
                  f"{fmt(rc / gc if rc and gc else None, '.1f')}x | "
                  f"{fmt(mean(rest, 'answer_f1'), '.2f')} | {fmt(mean(gql, 'answer_f1'), '.2f')} | {incomplete} |")


if __name__ == "__main__":
    main()
