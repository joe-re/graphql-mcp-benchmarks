# source me: environment for cc/run_cc.py (no ANTHROPIC_API_KEY: claude -p uses the subscription login)
export PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
export PATH="$PROJECT_ROOT/.tools/bin:$PROJECT_ROOT/bin:$PATH"
export GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token)"
export GITHUB_TOKEN="$GITHUB_PERSONAL_ACCESS_TOKEN"
export MODEL=claude-haiku-4-5
export APOLLO_BIN_VERSION=v1.14.0
