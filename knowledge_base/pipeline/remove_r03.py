#!/usr/bin/env python3
"""Remove only owner-authorized TIDBRepo row 181, with backup and read-back."""

import argparse
import fcntl
import getpass
import json
import sys
import urllib.parse
import warnings
from pathlib import Path

from submit_r03 import Client, DATA_PATH, DATABASE, ROOT, SubmissionError, all_rows, now, same_record, save

AUTHORIZATION = ROOT / "knowledge_base/reconciliations/reviews/2026-10-29-R03-removal.json"
RUN = ROOT / "knowledge_base/literature_updates/runs/20261029-r03-removal"


def remove(client, username, authorization, run, execute=False):
    if (authorization.get("deletion_authorized") is not True
            or authorization.get("tidbrepo_row_id") != 181
            or authorization.get("expected_row", {}).get("doi_1")
            != "https://doi.org/10.1007/s10021-019-00376-8"):
        raise SubmissionError("Explicit authorization for the exact row 181 is required.")
    expected = authorization["expected_row"]
    run.mkdir(parents=True, exist_ok=True)
    path = run / "api_removal_receipt.json"
    with (run / "api_removal.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        prior = json.loads(path.read_text()) if path.exists() else {}
        _, access = client.request(f"/api/v1/database/{DATABASE}/access/" + urllib.parse.quote(username, safe=""))
        if not isinstance(access, dict) or access.get("type") not in ("write_own", "write_all"):
            raise SubmissionError("Account does not have database write access.")
        before = all_rows(client)
        targets = [row for row in before if int(row["id"]) == 181]
        if not targets:
            receipt = {"status": "verified_absent", "checked_at": now(), "rows": len(before),
                       "delete_performed_this_call": False, "previous_receipt": prior}
            save(path, receipt)
            return receipt
        if len(targets) != 1 or not same_record(targets[0], expected):
            raise SubmissionError("Row 181 differs from the authorized record. No deletion attempted.")
        if prior.get("status") in ("sending", "deleted_unverified", "failed_or_ambiguous", "verified_removed", "verified_absent"):
            raise SubmissionError("Earlier removal requires reconciliation; no automatic retry.")
        if not execute:
            return {"status": "ready", "before_rows": len(before), "delete_performed_this_call": False}
        # Preserve all prior rows locally; only id AND source DOI are deletion keys.
        save(run / "authenticated-before.json", before)
        request = {"keys": {"id": 181, "doi_1": expected["doi_1"]}}
        receipt = {"status": "sending", "started_at": now(), "before_rows": len(before),
                   "removed_row": targets[0], "request": request, "delete_performed_this_call": False}
        save(path, receipt)
        try:
            status, _ = client.request(DATA_PATH, request, method="DELETE")
            receipt.update(status="deleted_unverified", http_status=status, delete_performed_this_call=True)
            save(path, receipt)
            if status != 202:
                raise SubmissionError("Unexpected deletion response. Check receipt before any retry.")
            after = all_rows(client)
            save(run / "authenticated-after.json", after)
            wanted = {int(r["id"]): r for r in before if int(r["id"]) != 181}
            actual = {int(r["id"]): r for r in after}
            if actual != wanted:
                raise SubmissionError("Post-removal verification failed; reconcile before retrying.")
            receipt.update(status="verified_removed", verified_at=now(), after_rows=len(after),
                           all_other_rows_unchanged=True)
            save(path, receipt)
            return receipt
        except Exception:
            receipt.update(status="failed_or_ambiguous", attention_required=True)
            save(path, receipt)
            raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="yusriy")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    if not sys.stdin.isatty():
        print("Run in an interactive local terminal so password input is hidden.", file=sys.stderr)
        return 2
    try:
        authorization = json.loads(AUTHORIZATION.read_text())
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            password = getpass.getpass("TIDBRepo password (hidden; not saved): ")
        client = Client(args.username, password)
        del password
        result = remove(client, args.username, authorization, RUN, args.execute)
        print(json.dumps({key: result.get(key) for key in ["status", "before_rows", "after_rows", "rows"]}))
        print("Local receipt:", RUN / "api_removal_receipt.json")
        return 0
    except (SubmissionError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        print("Cancelled; inspect the local receipt before retrying any interrupted removal.", file=sys.stderr)
        return 1
    except getpass.GetPassWarning:
        print("Terminal cannot hide password input; use a normal local terminal.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
