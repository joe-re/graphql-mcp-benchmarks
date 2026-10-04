# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""run_benchmark.py with Claude Code (`claude -p`) as the harness instead of Goose.

Everything except the agent process is the upstream runner, unmodified: task
rendering, recipe rendering, the logging proxy, the timeout, the budget kill and
meta.json. Only the `goose run ...` subprocess is swapped for cc/claude_shim.py,
and the harness version recorded in meta.json names Claude Code instead of Goose.

  PROJECT_ROOT=$PWD RUNS_DIR=$PWD/runs-cc/phase1 MODEL=claude-haiku-4-5 \
    uv run cc/run_cc.py
"""
import os
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cc"))

import models  # noqa: E402
import run_benchmark as rb  # noqa: E402

models.extend(rb._RUN_PRICING)

SHIM = ROOT / "cc" / "claude_shim.py"
_real_popen = subprocess.Popen


class _Subprocess:
    """rb's `subprocess`, with `goose ...` redirected to the shim."""

    def __getattr__(self, name):
        return getattr(subprocess, name)

    @staticmethod
    def Popen(cmd, *args, **kwargs):
        if isinstance(cmd, list) and cmd and cmd[0] == "goose":
            cmd = [sys.executable, str(SHIM), *cmd[2:]]
            # Own process group, so the runner's timeout kill reaches `claude -p` and
            # its MCP servers too. Killing only the shim left `claude` holding the
            # stdout pipe, and the runner then blocked until it exited on its own.
            proc = _real_popen(cmd, *args, start_new_session=True, **kwargs)
            proc.kill = lambda: _killpg(proc)
            return proc
        return _real_popen(cmd, *args, **kwargs)


def _killpg(proc) -> None:
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def _claude_version() -> str | None:
    try:
        out = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() or None


rb.subprocess = _Subprocess()
rb._HARNESS_VERSIONS = {
    "goose_version": None,
    "harness": "claude-code -p (cc/claude_shim.py)",
    "claude_code_version": _claude_version(),
    "apollo_mcp_version": rb.os.environ.get("APOLLO_BIN_VERSION") or None,
    "apollo_mcp_binary_version": None,
    "harness_platform": f"{rb.platform.system()}/{rb.platform.machine()}",
}

if __name__ == "__main__":
    rb.main()
