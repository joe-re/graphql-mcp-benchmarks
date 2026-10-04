# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6", "tiktoken>=0.7"]
# ///
"""Run condition M-R5 (Jev plan -> code fetch -> Claude answers with no tools).

  RUNS_DIR=runs-cc/jev MODEL=claude-haiku-4-5 uv run cc/jev/run_prefetch.py M3@20 M1@20:2

Each argument is TASK or TASK:REP (rep defaults to 1).

For each task: Jev plans (cc/jev/prefetch.py), code fetches from the lean REST
services, and `claude -p` answers from the request plus the fetched data, through the
same logging proxy as every other run. The answer is graded with grade.py, and the
fetched data is scored for pass-through exactly as a tool result would be.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "cc" / "jev")]

import grade  # noqa: E402
import parse_logs  # noqa: E402
import run_benchmark as rb  # noqa: E402
import tiktoken  # noqa: E402
from catalog import Catalog  # noqa: E402
import prefetch  # noqa: E402

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")
RUNS_DIR = Path(os.environ.get("RUNS_DIR", ROOT / "runs-cc" / "jev"))
PORT = os.environ.get("PORT", "8080")
ENC = tiktoken.get_encoding("cl100k_base")  # what the proxy counts tool results with


def system_prompt() -> str:
    """M-R1's instructions, with "tools" swapped for "the data provided"."""
    text = (ROOT / "recipes" / "recipe_m_r1.yaml").read_text()
    block = text.split("instructions: |", 1)[1].split("prompt: |", 1)[0]
    lines = [l[2:] if l.startswith("  ") else l for l in block.splitlines()]
    s = "\n".join(l for l in lines if "benchmark-run-id" not in l).strip()
    s = s.replace("using ONLY the tools available to you", "using ONLY the data provided with the request")
    s = s.replace("Every fact in your answer must come from a tool result", "Every fact in your answer must come from the provided data")
    s = s.replace("If you need something a tool\nresult does not contain, make another call rather than inferring it.",
                  "If you need something the data does\nnot contain, say so rather than inferring it.")
    return s


def start_proxy(run_dir: Path):
    env = dict(os.environ, PROXY_LOG=str(run_dir / "proxy.jsonl"), RUN_LABEL=str(run_dir.name), PORT=PORT)
    proc = subprocess.Popen(["uv", "run", str(ROOT / "proxy" / "anthropic_logging_proxy.py")], cwd=ROOT, env=env,
                            stdout=open(run_dir / "proxy_server.log", "w"), stderr=subprocess.STDOUT)
    for _ in range(60):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/__health", timeout=2)
            return proc
        except Exception:
            time.sleep(0.5)
    proc.kill()
    raise RuntimeError("proxy did not become healthy")


def run(task_id: str, tasks: dict, cat: Catalog, cells: dict, rep: int = 1) -> dict:
    task = tasks[task_id]
    run_dir = RUNS_DIR / "M-R5-lean" / MODEL / task_id / f"rep{rep}"
    run_dir.mkdir(parents=True, exist_ok=True)
    for f in run_dir.glob("*"):
        f.unlink()
    request = task["prompt_rendered"]

    t0 = time.time()
    plan = prefetch.plan(request, cat, str(run_dir / "jev.jsonl"))
    data = prefetch.fetch(plan, cat)
    data_json = json.dumps(data, separators=(",", ":"))
    prefetch_s = round(time.time() - t0, 2)
    (run_dir / "plan.json").write_text(json.dumps(plan, indent=1))
    (run_dir / "data.json").write_text(data_json)

    prompt = f"{request}\n\nData retrieved from the airline's REST APIs:\n```json\n{data_json}\n```"
    sysp = system_prompt()
    (run_dir / "system_prompt.txt").write_text(sysp)
    cmd = ["claude", "-p", prompt, "--model", MODEL, "--system-prompt", sysp, "--tools", "",
           "--strict-mcp-config", "--setting-sources", "", "--no-session-persistence", "--max-turns", "3",
           "--output-format", "stream-json", "--verbose"]
    env = dict(os.environ, ANTHROPIC_BASE_URL=f"http://127.0.0.1:{PORT}", MAX_THINKING_TOKENS="0",
               CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1")
    env.pop("ANTHROPIC_API_KEY", None)
    proxy = start_proxy(run_dir)
    try:
        with tempfile.TemporaryDirectory(prefix="cc-run-") as cwd:
            t1 = time.time()
            proc = subprocess.run(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                  timeout=420)
            answer_s = round(time.time() - t1, 2)
    finally:
        proxy.terminate()
        proxy.wait(timeout=10)
    (run_dir / "stream.jsonl").write_text(proc.stdout)
    result = next((json.loads(l) for l in proc.stdout.splitlines() if '"type":"result"' in l), {})
    answer = result.get("result") or ""
    (run_dir / "stdout.txt").write_text(answer)

    usage = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
    n_calls = 0
    for line in (run_dir / "proxy.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r.get("is_messages"):
            n_calls += 1
            for k in usage:
                usage[k] += r.get(k) or 0
    jev_calls = [json.loads(l) for l in (run_dir / "jev.jsonl").read_text().splitlines()]

    graded = grade.grade(cells[task_id], grade.final_answer(answer))
    synthetic = [{"call": 1, "tool_use": [{"id": "prefetch", "name": "prefetch", "input": {}}],
                  "tool_result": [{"tool_use_id": "prefetch", "is_error": False, "bytes": len(data_json),
                                   "content": data_json}]}]
    pt = grade.pass_through_tokens(synthetic, grade.final_answer(answer))
    data_tokens = len(ENC.encode(data_json))
    out = {
        "condition": "M-R5", "profile": "lean", "model": MODEL, "task_id": task_id, "rep": rep,
        "claude_inference_calls": n_calls, "claude_usage": usage,
        "data_bytes": len(data_json), "data_tokens_cl100k": data_tokens,
        "pass_through_tokens": round((pt.get("pass_through_fraction") or 0) * data_tokens),
        "pass_through_fraction": pt.get("pass_through_fraction"),
        "answer_f1": graded.get("answer_f1"), "answer_coverage": graded.get("coverage"),
        "jev_calls": len(jev_calls), "jev_input_tokens": sum(c["usage"]["input_tokens"] for c in jev_calls),
        "jev_cost_usd": sum(c["cost_usd"] for c in jev_calls),
        "prefetch_s": prefetch_s, "answer_s": answer_s, "claude_exit": proc.returncode,
        "claude_code_version": subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip(),
    }
    (run_dir / "result.json").write_text(json.dumps(out, indent=1))
    return out


def main():
    tasks = {t["id"]: t for t in rb.load_tasks()}
    cells = parse_logs.expected_cells()
    cat = Catalog()
    for spec in sys.argv[1:]:
        task_id, _, rep = spec.partition(":")
        r = run(task_id, tasks, cat, cells, int(rep or 1))
        print(json.dumps({k: r[k] for k in ("model", "task_id", "rep", "claude_inference_calls", "data_tokens_cl100k",
                                            "pass_through_tokens", "answer_f1", "jev_cost_usd", "claude_exit")}),
              flush=True)


if __name__ == "__main__":
    main()
