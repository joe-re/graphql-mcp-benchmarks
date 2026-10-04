"""Jev experiments and their baselines, three reps each: mean ± sd per model, task and condition.

  python3 cc/jev/summarize.py > results-cc/jev/summary_3reps.md

Reads results-cc/{phase2,phase2-factors,phase2-bff,jev}/<model>/raw.csv (parse_with_prices
output) and results-cc/jev/{m_r5,jev_cost}.csv (cc/jev/export_runs.py output). Cost is
API-equivalent, with cache writes at the 1-hour TTL price (2x input), as for every claude -p row.
"""
import csv, statistics, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "cc")]
import models, parse_logs as P  # noqa: E402
models.extend(P._PRICING)
K = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
num = lambda v: float(v) if v not in (None, "") else 0.0
MODELS = ("claude-haiku-4-5", "claude-sonnet-5")
CONDS = ("M-R1-lean", "M-R4-lean", "M-G2", "M-G3", "M-R6-lean", "M-R7-lean", "M-R8-lean")


def cost(u, m):
    p = P._price_for(m)
    return (u["input_tokens"] * p["input"] + u["output_tokens"] * p["output"]
            + u["cache_read_input_tokens"] * p["cache_read"] + u["cache_creation_input_tokens"] * p["input"] * 2.0) / 1e6


def rows(p):
    try:
        return list(csv.DictReader(open(p)))
    except FileNotFoundError:
        return []


def ms(v, fmt):
    v = list(v)
    if not v:
        return "—"
    s = f" ± {fmt.format(statistics.stdev(v))}" if len(v) > 1 else ""
    return fmt.format(statistics.mean(v)) + s


M_R5 = rows(ROOT / "results-cc/jev/m_r5.csv")
JEV_COST = {(r["model"], r["cell"], r["task_id"], r["rep"]): num(r["jev_cost_usd"])
            for r in rows(ROOT / "results-cc/jev/jev_cost.csv")}


def main():
    print("Jev の実験と比較対象（各 3 回）。値は平均 ± 標準偏差。コストは API 料金換算"
          "（キャッシュ書き込みは 1 時間 TTL = 入力の 2 倍）。Jev の費用は別の列。\n")
    for task in ("M3@20", "M1@20", "M2@1"):
        print(f"\n### {task}\n\n| モデル | 条件 | n | ツール呼び出し | 推論 | ツール結果 / データ | Claude の入力合計 "
              f"| $/回（Claude） | Jev $/回 | f1 |\n|---|---|--:|--:|--:|--:|--:|--:|--:|--:|")
        for m in MODELS:
            allr = sum((rows(ROOT / f"results-cc/{d}/{m}/raw.csv") for d in ("phase2", "phase2-factors", "phase2-bff", "jev")), [])
            for c in CONDS:
                rs = [r for r in allr if r["cell"] == c and r["task_id"] == task]
                if not rs:
                    continue
                jevc = [JEV_COST[(m, c, task, r["rep"])] for r in rs] if c in ("M-R6-lean", "M-R7-lean", "M-R8-lean") else []
                tin = [num(r["proxy_input_tokens"]) + num(r["proxy_cache_read_input_tokens"]) + num(r["proxy_cache_creation_input_tokens"]) for r in rs]
                cst = [cost({k: num(r["proxy_" + k]) for k in K}, m) for r in rs]
                print(f"| {m[7:]} | {c} | {len(rs)} | {ms([num(r['proxy_n_tool_calls']) for r in rs], '{:.1f}')} "
                      f"| {ms([num(r['proxy_n_inference_calls']) for r in rs], '{:.1f}')} | {ms([num(r['proxy_tool_result_tokens']) for r in rs], '{:,.0f}')} "
                      f"| {ms(tin, '{:,.0f}')} | {ms(cst, '{:.4f}')} | {ms(jevc, '{:.4f}') if jevc else '—'} | {ms([num(r['answer_f1']) for r in rs], '{:.2f}')} |")
            rs = [r for r in M_R5 if r["model"] == m and r["task_id"] == task]
            if rs:
                u = [{k: num(r[k]) for k in K} for r in rs]
                print(f"| {m[7:]} | M-R5-lean (A) | {len(rs)} | 0 | {ms([num(r['claude_inference_calls']) for r in rs], '{:.1f}')} "
                      f"| {ms([num(r['data_tokens_cl100k']) for r in rs], '{:,.0f}')} "
                      f"| {ms([x['input_tokens'] + x['cache_read_input_tokens'] + x['cache_creation_input_tokens'] for x in u], '{:,.0f}')} "
                      f"| {ms([cost(x, m) for x in u], '{:.4f}')} | {ms([num(r['jev_cost_usd']) for r in rs], '{:.4f}')} | {ms([num(r['answer_f1']) for r in rs], '{:.2f}')} |")


if __name__ == "__main__":
    main()
