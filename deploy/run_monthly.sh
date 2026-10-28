#!/usr/bin/env bash
set -euo pipefail

DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$DEPLOY_DIR/.." && pwd)"
PYTHON_BIN="$PROJECT_DIR/.venv/bin/python"
RUNS_DIR="$PROJECT_DIR/knowledge_base/literature_updates/runs"
STATE_DIR="$PROJECT_DIR/knowledge_base/literature_updates/state"

mkdir -p "$RUNS_DIR" "$STATE_DIR"
exec 9>"$STATE_DIR/monthly-run.lock"
if ! flock -n 9; then
  echo "A monthly literature run is already active; exiting."
  exit 0
fi

# Keep the existing service and timer unchanged; delegate only the run body.
# Fall back to system Python so missing venv dependencies still produce a failure summary.
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="$(command -v python3)"
fi
exec "$PYTHON_BIN" "$PROJECT_DIR/knowledge_base/pipeline/monthly_research.py" run
