# source me: environment for cc/run_goose_nosampling.py (Goose + the API key in .env)
export PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
export PATH="$PROJECT_ROOT/.tools/bin:$PROJECT_ROOT/bin:$PATH"
set -a; . "$PROJECT_ROOT/.env"; set +a
export GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token)"
export GITHUB_TOKEN="$GITHUB_PERSONAL_ACCESS_TOKEN"
export APOLLO_BIN_VERSION=v1.14.0
export B2_BIN=cc/rover_schema_mcp.sh   # TLS-safe Python for condition B2 (see cc/README.md)
export PER_RUN_BUDGET_USD=3
