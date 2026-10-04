#!/usr/bin/env bash
# Baselines used in the Jev comparison, reps 2 and 3 (rep 1 ran in cc/run_factors.sh and cc/bff/).
# Same conditions as rep 1: REST in the lean profile, BFF on :4004.
set -euo pipefail
cd "$(dirname "$0")/.."
source cc/env.sh
export PROJECT_ROOT=$PWD PAYLOAD_PROFILE=lean
python3 cc/bff/bff_server.py --port 4004 > runs-cc/bff_server.log 2>&1 &
BFF=$!
trap 'kill $BFF 2>/dev/null || true' EXIT
for i in $(seq 1 20); do curl -sf localhost:4004/__health >/dev/null && break; sleep 0.5; done
for m in claude-haiku-4-5 claude-sonnet-5; do
  for rep in 2 3; do
    echo "===== $m rep$rep"
    MODEL=$m RUNS_DIR="$PWD/runs-cc/phase2-factors/$m" caffeinate -i -s uv run cc/rerun_cc.py \
      M-R1:M3@20:$rep M-G3:M3@20:$rep M-R1:M1@20:$rep M-R1:M2@1:$rep M-G2:M2@1:$rep M-G3:M2@1:$rep
    MODEL=$m RUNS_DIR="$PWD/runs-cc/phase2-bff/$m" caffeinate -i -s uv run cc/bff/run_bff.py M-R4:M3@20:$rep
  done
done
