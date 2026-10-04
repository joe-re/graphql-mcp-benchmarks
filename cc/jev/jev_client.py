"""Minimal client for TypeSafe's System One API (Jev). Standard library only.

    POST https://api.typesafe.ai/v1/systemone
    Authorization: Bearer $JEV_API_KEY

Every request and response is appended to a JSONL log when `log_path` is given, so
the token cost of each Jev call can be totalled separately from Claude's.
Reference: https://docs.typesafe.ai/api.md
"""
import json
import os
import time
import urllib.error
import urllib.request

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODEL = os.environ.get("JEV_MODEL", "jev-1.13.0")
PRICE_PER_MTOK = 0.042  # input tokens only; output is free (docs.typesafe.ai/models.md)


def ask(state, questions: dict, log_path=None, label="", retries=4) -> dict:
    """One System One call. `questions` maps an id to a Noul / Choice / Score question."""
    key = os.environ.get("JEV_API_KEY")
    if not key:
        raise SystemExit("JEV_API_KEY is not set (put it in .env)")
    body = json.dumps({"state": state, "model": MODEL, "questions": questions}).encode()
    for attempt in range(retries):
        req = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={
            "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        started = time.time()
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.load(resp)
            break
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:500]
            if e.code == 429 and attempt < retries - 1:
                time.sleep(float(e.headers.get("retry-after") or 2 ** attempt))
                continue
            raise RuntimeError(f"Jev HTTP {e.code}: {detail}") from None
    if log_path:
        with open(log_path, "a") as f:
            f.write(json.dumps({
                "label": label, "model": result.get("model"), "n_questions": len(questions),
                "usage": result.get("usage"), "duration_s": round(time.time() - started, 3),
                "cost_usd": (result.get("usage") or {}).get("input_tokens", 0) * PRICE_PER_MTOK / 1e6,
                "questions": questions, "answers": result.get("answers"),
            }) + "\n")
    return result


def noul(instructions, true=None, false=None) -> dict:
    q = {"type": "noul", "instructions": instructions}
    if true or false:
        q["criteria"] = {k: v for k, v in (("true", true), ("false", false)) if v}
    return q


def choice(instructions, options: dict) -> dict:
    return {"type": "choice", "instructions": instructions, "criteria": options}
