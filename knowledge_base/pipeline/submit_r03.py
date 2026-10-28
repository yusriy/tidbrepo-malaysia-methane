#!/usr/bin/env python3
"""One-time, owner-authorized R03 submission; credentials stay in memory."""

from __future__ import annotations

import argparse
import base64
import fcntl
import getpass
import json
import math
import sys
import urllib.error
import urllib.parse
import urllib.request
import warnings
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "knowledge_base/reconciliations/reviews/2026-10-29-R03-upload.json"
RUN = ROOT / "knowledge_base/literature_updates/runs/20261028-r03-upload"
BASE = "https://tidbrepo.usm.my"
DATABASE = "8cb5b734-7d57-4ca5-81a6-4d1de7acee88"
TABLE = "ff844ee0-03d8-4531-ae43-14f4bbdf4cd4"
DATA_PATH = f"/api/v1/database/{DATABASE}/table/{TABLE}/data"
DOI = "10.1007/s10021-019-00376-8"


class SubmissionError(Exception):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    # Never forward the Basic credential to a redirect destination.
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Client:
    def __init__(self, username, password):
        if not username or ":" in username or not password:
            raise SubmissionError("A username and nonempty password are required.")
        self.authorization = "Basic " + base64.b64encode(
            f"{username}:{password}".encode()
        ).decode()
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, path, data=None):
        if not path.startswith("/api/v1/") or path.startswith("//"):
            raise SubmissionError("Request is outside the fixed TIDBRepo API.")
        request = urllib.request.Request(
            BASE + path,
            data=None if data is None else json.dumps(data).encode(),
            headers={"Authorization": self.authorization, "Accept": "application/json",
                     "Content-Type": "application/json"},
            method="GET" if data is None else "POST",
        )
        try:
            with self.opener.open(request, timeout=60) as response:
                content = response.read()
                return response.status, json.loads(content) if content else None
        except urllib.error.HTTPError as error:
            # Do not print server bodies, request objects, or credentials.
            raise SubmissionError(f"TIDBRepo returned HTTP {error.code}.") from None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            raise SubmissionError("Request failed or response was unreadable; check receipt before retrying.") from None


def all_rows(client):
    rows = []
    for page in range(100):
        _, batch = client.request(DATA_PATH + f"?page={page}&size=1000")
        if not isinstance(batch, list):
            raise SubmissionError("Unexpected table response; no submission attempted.")
        if not batch:
            if len({int(r["id"]) for r in rows}) != len(rows):
                raise SubmissionError("Pagination repeated rows; table completeness uncertain.")
            return rows
        rows.extend(batch)
    raise SubmissionError("Table pagination did not terminate; no submission attempted.")


def same_record(row, payload):
    for key, value in payload.items():
        actual = row.get(key)
        if key in ("mean", "stdev", "tier"):
            try:
                if not math.isclose(float(actual), float(value), rel_tol=1e-10, abs_tol=1e-12):
                    return False
            except (TypeError, ValueError):
                return False
        elif value is None:
            if actual not in (None, ""):
                return False
        elif str(actual).strip() != str(value).strip():
            return False
    return True


def validated_payload(package):
    if package.get("authorization", {}).get("tidbrepo_upload_authorized") is not True:
        raise SubmissionError("Owner upload authorization is missing.")
    payload = package.get("payload", [])
    if len(payload) != 1 or package.get("doi") != DOI:
        raise SubmissionError("Only the approved single R03 record may be submitted.")
    row = payload[0]
    if (row.get("doi_1") != "https://doi.org/" + DOI
            or row.get("countries") != "Malaysia" or row.get("category") != "Peat lands"
            or row.get("mean") != 0.158 or row.get("stdev") != 0.144
            or row.get("unit") != "kg CH₄ ha⁻¹ day⁻¹"
            or row.get("min") is not None or row.get("max") is not None
            or not all(s in row.get("condition", "") for s in ["Undrained", "Maludam", "non-trenched", "n=9", "outlier excluded"])):
        raise SubmissionError("R03 payload differs from the source-checked representation.")
    return row


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def submit(client, username, package, run, execute=False):
    payload = validated_payload(package)
    run.mkdir(parents=True, exist_ok=True)
    receipt_path = run / "api_submission_receipt.json"
    with (run / "api_submission.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        prior = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
        access_path = f"/api/v1/database/{DATABASE}/access/" + urllib.parse.quote(username, safe="")
        _, access = client.request(access_path)
        if not isinstance(access, dict) or access.get("type") not in ("write_own", "write_all"):
            raise SubmissionError("Account does not have database write access.")
        rows = all_rows(client)
        source_rows = [r for r in rows if any(
            DOI in str(r.get(f"doi_{i}", "")).lower() for i in range(1, 7))]
        exact = [r for r in source_rows if same_record(r, payload)]
        if len(exact) == 1 and len(source_rows) == 1:
            receipt = {"status": "verified_existing", "checked_at": now(),
                       "row": exact[0], "rows": len(rows), "insert_performed_this_call": False}
            if prior:
                receipt["previous_receipt"] = prior
            save(receipt_path, receipt)
            return receipt
        if source_rows:
            raise SubmissionError("R03 DOI already exists with different or multiple records; reconcile before inserting.")
        if prior.get("status") in ("sending", "submitted_unverified", "failed_or_ambiguous", "verified", "verified_existing"):
            raise SubmissionError("Earlier submission is unresolved or was previously verified. No automatic retry.")
        if not execute:
            return {"status": "ready", "rows": len(rows), "insert_performed_this_call": False}
        # Explicit primary key avoids assumptions about auto-increment. A concurrent
        # insertion may reject this ID; it must never trigger a blind retry.
        record = {"id": max((int(r["id"]) for r in rows), default=0) + 1, **payload}
        receipt = {"status": "sending", "started_at": now(), "before_rows": len(rows),
                   "request": {"data": record}, "insert_performed_this_call": False}
        save(receipt_path, receipt)
        try:
            status, _ = client.request(DATA_PATH, {"data": record})
            receipt.update(status="submitted_unverified", http_status=status,
                           insert_performed_this_call=True)
            save(receipt_path, receipt)
            if status != 201:
                raise SubmissionError("Insert response was not HTTP 201; verify manually before retrying.")
            after = all_rows(client)
            new = [r for r in after if str(r.get("id")) == str(record["id"]) and same_record(r, payload)]
            old = {int(r["id"]): r for r in rows}
            current = {int(r["id"]): r for r in after}
            if len(new) != 1 or any(current.get(i) != r for i, r in old.items()):
                raise SubmissionError("Post-insert verification failed; do not retry automatically.")
            receipt.update(status="verified", verified_at=now(), row=new[0], after_rows=len(after))
            save(receipt_path, receipt)
            return receipt
        except Exception:
            receipt.update(status="failed_or_ambiguous", attention_required=True)
            save(receipt_path, receipt)
            raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="yusriy")
    parser.add_argument("--execute", action="store_true", help="Submit the owner-authorized R03 record after checks")
    args = parser.parse_args(argv)
    if not sys.stdin.isatty():
        print("Run in an interactive terminal; password input must be hidden.", file=sys.stderr)
        return 2
    try:
        package = json.loads(PACKAGE.read_text())
        validated_payload(package)
        # Refuse getpass's echoing fallback if a terminal cannot hide input.
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            password = getpass.getpass("TIDBRepo password (hidden; not saved): ")
        client = Client(args.username, password)
        del password
        result = submit(client, args.username, package, RUN, args.execute)
        print(json.dumps({k: result.get(k) for k in ["status", "rows", "after_rows"]}))
        if result.get("row"):
            print("Verified TIDBRepo row:", result["row"]["id"])
        print("Local receipt:", RUN / "api_submission_receipt.json")
        return 0
    except (SubmissionError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        print("Cancelled; check the local receipt before retrying any interrupted submission.", file=sys.stderr)
        return 1
    except getpass.GetPassWarning:
        print("Terminal cannot hide password input; use a normal local terminal.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
