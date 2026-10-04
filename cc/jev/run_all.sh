#!/usr/bin/env bash
# Jev experiments (2026-10-01): A = M-R5 (plan+fetch, no tools), B = M-R6 (tool gate), C = M-R7 (response prune).
# One rep each, Haiku 4.5 and Sonnet 5, REST in the lean profile.
set -euo pipefail
cd "$(dirname "$0")/../.."
source cc/env.sh
set -a; . ./.env; set +a
export PROJECT_ROOT=$PWD PAYLOAD_PROFILE=lean
for m in claude-haiku-4-5 claude-sonnet-5; do
  echo "===== $m"
  tasks="M3@20 M1@20 M2@1"; [ "$m" = claude-haiku-4-5 ] && tasks="M3@20 M1@20"   # Haiku M2@1 ran as the smoke test
  MODEL=$m RUNS_DIR=$PWD/runs-cc/jev caffeinate -i -s uv run cc/jev/run_prefetch.py $tasks
  MODEL=$m RUNS_DIR=$PWD/runs-cc/jev/$m caffeinate -i -s uv run cc/jev/run_bc.py M-R6:M3@20:1 M-R7:M3@20:1
done
