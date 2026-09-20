# Ubuntu monthly Malaysian methane literature check

This package performs a deterministic monthly candidate search. It uses OpenAlex and local PDF text extraction; it does not call OpenAI and it never uploads to TIDBRepo.

## What the scheduled run does

1. Searches for post-26-August-2023 Malaysian methane literature.
2. Removes records already represented in the knowledge database, the current 180-row TIDBRepo snapshot, or any earlier monthly run.
3. Downloads open-access PDFs when available.
4. Extracts page-traceable candidate values.
5. Produces `candidate_review.csv`, `review.csv`, `REVIEW.md`, and `READY_FOR_REVIEW.txt`.
6. Stops for human review.

The timer cannot invoke the upload command. No TIDBRepo credential is included in this package.

## Copy through AnyDesk

1. Connect to the Ubuntu laptop in AnyDesk.
2. Select **File Transfer** and copy `tidbrepo-monthly-ubuntu.tar.gz` to the remote `Downloads` directory.
3. Open a terminal on the remote laptop and run:

```bash
mkdir -p ~/tidbrepo-monthly
tar -xzf ~/Downloads/tidbrepo-monthly-ubuntu.tar.gz -C ~/tidbrepo-monthly
cd ~/tidbrepo-monthly
./deploy/install_ubuntu.sh YOUR_EMAIL_ADDRESS
```

The email address is sent only as the polite contact address in OpenAlex requests. It is not an OpenAI or TIDBRepo credential.

If Ubuntu reports that virtual-environment support is missing:

```bash
sudo apt update
sudo apt install python3-venv
./deploy/install_ubuntu.sh YOUR_EMAIL_ADDRESS
```

## Test the installation

```bash
systemctl --user start --no-block tidbrepo-monthly.service
journalctl --user -fu tidbrepo-monthly.service
systemctl --user list-timers tidbrepo-monthly.timer
```

`systemctl start` normally waits for this one-shot service to finish, which can take several minutes. `--no-block` returns the terminal prompt immediately; the following `journalctl -f` command displays progress. Press `Ctrl+C` to leave the live log without stopping the literature run.

For a non-following status check:

```bash
systemctl --user status tidbrepo-monthly.service --no-pager
journalctl --user -u tidbrepo-monthly.service -n 100 --no-pager
```

The newest output path is recorded in:

```text
~/tidbrepo-monthly/knowledge_base/literature_updates/state/latest_run_path.txt
```

## Run while logged out

For a user timer to run after the account logs out, enable lingering once:

```bash
sudo loginctl enable-linger "$USER"
```

This is optional when the AnyDesk user's desktop session remains logged in.

## Review and update boundary

- `candidate_review.csv` is the first human gate.
- `review.csv` is the value-level gate after source verification.
- Database payload preparation remains manual.
- TIDBRepo upload remains a separate, explicit operation after approval.
