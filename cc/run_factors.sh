#!/usr/bin/env bash
# Factor isolation runs (2026-09-29): one rep each, Haiku 4.5 and Sonnet 5, stack in the lean profile.
#   A  field selection : M-R1(lean) x M1@20            (compare M-R1-fat / M-G2 from runs-cc/phase2)
#   B  join ownership  : M-R1(lean), M-G3 x M3@20
#   C  discovery cost  : M-R1(lean), M-G2, M-G3 x M2@1
set -euo pipefail
cd "$(dirname "$0")/.."
specs=(M-R1:M1@20:1 M-R1:M3@20:1 M-G3:M3@20:1 M-R1:M2@1:1 M-G2:M2@1:1 M-G3:M2@1:1)
source cc/env.sh
for m in claude-haiku-4-5 claude-sonnet-5; do
  echo "===== $m"
  PAYLOAD_PROFILE=lean MODEL=$m RUNS_DIR="$PWD/runs-cc/phase2-factors/$m" \
    caffeinate -i -s uv run cc/rerun_cc.py "${specs[@]}"
done
