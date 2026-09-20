#!/usr/bin/env bash
set -euo pipefail

DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$DEPLOY_DIR/.." && pwd)"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
ENV_FILE="$HOME/.config/tidbrepo-monthly.env"
CONTACT_EMAIL="${1:-}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required. Install python3 and python3-venv, then rerun this installer." >&2
  exit 2
fi

if ! python3 -m venv "$PROJECT_DIR/.venv" 2>/dev/null; then
  echo "Could not create a virtual environment." >&2
  echo "On Ubuntu, run: sudo apt install python3-venv" >&2
  exit 2
fi

"$PROJECT_DIR/.venv/bin/python" -m pip install --upgrade pip
"$PROJECT_DIR/.venv/bin/python" -m pip install -r "$PROJECT_DIR/knowledge_base/requirements.txt"
cd "$PROJECT_DIR"
"$PROJECT_DIR/.venv/bin/python" -m unittest knowledge_base.tests.test_tidbrepo_literature_update -q

mkdir -p "$SYSTEMD_USER_DIR" "$(dirname "$ENV_FILE")"
sed "s|__INSTALL_DIR__|$PROJECT_DIR|g" \
  "$DEPLOY_DIR/tidbrepo-monthly.service.in" \
  > "$SYSTEMD_USER_DIR/tidbrepo-monthly.service"
cp "$DEPLOY_DIR/tidbrepo-monthly.timer" "$SYSTEMD_USER_DIR/tidbrepo-monthly.timer"

if [[ -n "$CONTACT_EMAIL" ]]; then
  printf 'TIDBREPO_CONTACT_EMAIL=%q\n' "$CONTACT_EMAIL" > "$ENV_FILE"
elif [[ ! -f "$ENV_FILE" ]]; then
  printf '%s\n' '# Optional: TIDBREPO_CONTACT_EMAIL=your-email@example.org' > "$ENV_FILE"
fi
chmod 600 "$ENV_FILE"

systemctl --user daemon-reload
systemctl --user enable --now tidbrepo-monthly.timer

echo
echo "Installation complete."
echo "Project: $PROJECT_DIR"
echo "Timer: first day of each month at 03:15, with up to 45 minutes randomized delay"
echo "Status: systemctl --user list-timers tidbrepo-monthly.timer"
echo "Test: systemctl --user start --no-block tidbrepo-monthly.service"
echo "Logs: journalctl --user -u tidbrepo-monthly.service -n 100 --no-pager"
echo "No automatic TIDBRepo upload is configured."
