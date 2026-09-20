#!/usr/bin/env bash
set -euo pipefail

DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$DEPLOY_DIR/.." && pwd)"
PYTHON_BIN="$PROJECT_DIR/.venv/bin/python"
PIPELINE="$PROJECT_DIR/knowledge_base/pipeline/tidbrepo_literature_update.py"
RUNS_DIR="$PROJECT_DIR/knowledge_base/literature_updates/runs"
STATE_DIR="$PROJECT_DIR/knowledge_base/literature_updates/state"

mkdir -p "$RUNS_DIR" "$STATE_DIR"
exec 9>"$STATE_DIR/monthly-run.lock"
if ! flock -n 9; then
  echo "A monthly literature run is already active; exiting."
  exit 0
fi

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Missing Python environment: $PYTHON_BIN" >&2
  echo "Run deploy/install_ubuntu.sh first." >&2
  exit 2
fi

discover_args=(
  "$PYTHON_BIN"
  "$PIPELINE"
  discover
  --runs-dir "$RUNS_DIR"
)
if [[ -n "${TIDBREPO_CONTACT_EMAIL:-}" ]]; then
  discover_args+=(--mailto "$TIDBREPO_CONTACT_EMAIL")
fi

run_id="$(date -u +%Y%m%dT%H%M%SZ)"
run_dir="$RUNS_DIR/$run_id"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Starting discovery run $run_id"
"${discover_args[@]}" --run-id "$run_id"

if [[ ! -d "$run_dir" ]]; then
  echo "Discovery did not return a valid run directory: $run_dir" >&2
  exit 3
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Extracting values from available open-access PDFs"
"$PYTHON_BIN" "$PIPELINE" extract "$run_dir"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Building human-review files"
"$PYTHON_BIN" "$PIPELINE" review "$run_dir"

candidate_count="$(wc -l < "$run_dir/candidates.jsonl" | tr -d ' ')"
proposal_count="$(wc -l < "$run_dir/proposals.jsonl" | tr -d ' ')"
printf '%s\n' "$run_dir" > "$STATE_DIR/latest_run_path.txt"

{
  echo "Monthly Malaysian methane literature check completed."
  echo "Run directory: $run_dir"
  echo "New candidate papers: $candidate_count"
  echo "Automatically proposed values: $proposal_count"
  echo "Review candidate_review.csv before any further extraction or database preparation."
  echo "No TIDBRepo upload was attempted."
} > "$run_dir/READY_FOR_REVIEW.txt"

cat "$run_dir/READY_FOR_REVIEW.txt"
