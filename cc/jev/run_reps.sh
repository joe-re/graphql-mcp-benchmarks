#!/usr/bin/env bash
# Jev experiments, reps 2 and 3 (rep 1 ran in cc/jev/run_all.sh and the M-R8 pass). Same code, same questions.
set -euo pipefail
cd "$(dirname "$0")/../.."
source cc/env.sh
set -a; . ./.env; set +a
export PROJECT_ROOT=$PWD PAYLOAD_PROFILE=lean
for m in claude-haiku-4-5 claude-sonnet-5; do
  for rep in 2 3; do
    echo "===== $m rep$rep"
    MODEL=$m RUNS_DIR=$PWD/runs-cc/jev caffeinate -i -s uv run cc/jev/run_prefetch.py M3@20:$rep M1@20:$rep M2@1:$rep
    MODEL=$m RUNS_DIR=$PWD/runs-cc/jev/$m caffeinate -i -s uv run cc/jev/run_bc.py \
      M-R6:M3@20:$rep M-R7:M3@20:$rep M-R8:M3@20:$rep M-R8:M1@20:$rep
  done
done
