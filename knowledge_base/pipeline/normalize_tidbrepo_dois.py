#!/usr/bin/env python3
"""Apply only the owner's frozen DOI-format changes; never modifies factors."""
import argparse
import fcntl
import getpass
import hashlib
import json
import sys
import urllib.parse
import warnings
from pathlib import Path

from doi_identifiers import validated_doi
from factor_plausibility import fetch_rows
from submit_r03 import Client, DATABASE, DATA_PATH, ROOT, SubmissionError, all_rows, now, save

PLAN = ROOT / 'knowledge_base/reconciliations/reviews/2026-10-29-doi-normalization.json'
RUN = ROOT / 'knowledge_base/literature_updates/runs/20261029-defaults-and-doi/doi-update'
DOI_FIELDS = {f'doi_{i}' for i in range(1, 7)}


def fingerprint(row):
    return hashlib.sha256(json.dumps(row, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def validate_plan(plan):
    if plan.get('doi_format_update_authorized') is not True or plan.get('canonical_format') != 'lowercase bare DOI':
        raise SubmissionError('Explicit DOI-format authorization is required.')
    seen = set()
    for patch in plan.get('patches', []):
        if not isinstance(patch['id'], int) or patch['id'] in seen or patch['id'] == 181:
            raise SubmissionError('Invalid or repeated target ID.')
        seen.add(patch['id'])
        old, new = patch['before'], patch['after']
        if not old or set(old) != set(new) or not set(old) <= DOI_FIELDS:
            raise SubmissionError('Only existing DOI fields may be updated.')
        for key in old:
            if new[key] != validated_doi(old[key]) or new[key] == old[key]:
                raise SubmissionError('Patch changes DOI identity or is not canonical.')
    return plan['patches']


def expected_row(row, patch):
    changed = dict(row)
    changed.update(patch['after'])
    return changed


def reconcile(plan, run, rows):
    patches = validate_plan(plan)
    with (run / 'update.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        path = run / 'receipt.json'
        prior = json.loads(path.read_text())
        original = {r['id']: r for r in json.loads((run / 'before.json').read_text())}
        current = {r['id']: r for r in rows}
        if set(current) != set(original):
            raise SubmissionError('Record IDs changed; manual reconciliation required.')
        by_id = {p['id']: p for p in patches}
        completed, pending = [], []
        for row_id, old in original.items():
            patch = by_id.get(row_id)
            if patch and current[row_id] == expected_row(old, patch):
                completed.append(row_id)
            elif current[row_id] == old:
                if patch: pending.append(row_id)
            else:
                raise SubmissionError('Unexpected table change; manual reconciliation required.')
        if prior.get('status') not in ('failed_or_ambiguous', 'sending'):
            raise SubmissionError('Only an unresolved attempt needs reconciliation.')
        stamp = now().replace(':', '-')
        save(run / f'reconciliation-{stamp}.json', {'checked_at': now(), 'completed_ids': completed, 'pending_ids': pending, 'all_other_fields_unchanged': True})
        receipt = {'status': 'reconciled_pending' if pending else 'verified', 'checked_at': now(),
                   'completed_ids': completed, 'pending_ids': pending, 'previous_receipt': prior,
                   'non_doi_fields_unchanged': True}
        save(path, receipt)
        return receipt


def apply(client, username, plan, run, execute=False, reader=None):
    patches = validate_plan(plan)
    run.mkdir(parents=True, exist_ok=True)
    receipt_path = run / 'receipt.json'
    with (run / 'update.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        prior = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
        if prior.get('status') in ('sending', 'failed_or_ambiguous'):
            raise SubmissionError('Prior attempt needs reconciliation; no automatic retry.')
        try:
            before = reader() if reader is not None else all_rows(client)
        except SubmissionError as error:
            if 'HTTP 401' in str(error):
                raise SubmissionError('HTTP 401: TIDBRepo rejected authentication during the read-only preflight. No DOI updates attempted. Check the exact TIDBRepo username and password; use --username if different from yusriy.') from None
            raise
        by_id = {r['id']: r for r in before}
        pending = []
        for patch in patches:
            row = by_id.get(patch['id'])
            if row is None:
                raise SubmissionError('Target row is missing.')
            if all(row.get(k) == v for k, v in patch['after'].items()):
                continue
            if fingerprint(row) != patch['row_sha256'] or any(row.get(k) != v for k, v in patch['before'].items()):
                raise SubmissionError('A target row changed since the plan; no update attempted.')
            pending.append(patch)
        if not pending:
            return {'status': 'verified_already_canonical', 'rows': len(before), 'updates': 0}
        if not execute:
            return {'status': 'ready', 'rows': len(before), 'updates': len(pending), 'fields': sum(len(p['after']) for p in pending)}
        _, access = client.request(f'/api/v1/database/{DATABASE}/access/' + urllib.parse.quote(username, safe=''))
        if not isinstance(access, dict) or access.get('type') not in ('write_own', 'write_all'):
            raise SubmissionError('Account lacks database write access.')
        if not (run / 'before.json').exists():
            save(run / 'before.json', before)
        save(run / ('attempt-before-' + now().replace(':', '-') + '.json'), before)
        receipt = {'status': 'sending', 'started_at': now(), 'confirmed_ids': [],
                   'plan_sha256': fingerprint(plan), 'before_rows': len(before), 'previous_receipt': prior}
        save(receipt_path, receipt)
        wanted = dict(by_id)
        try:
            for patch in pending:
                # Keys bind the ID and original DOI strings; data cannot include a
                # factor, category, condition, unit, source URL or verification field.
                payload = {'keys': {'id': patch['id'], **patch['before']}, 'data': patch['after']}
                receipt['stage'] = f'write_row_{patch["id"]}'
                save(receipt_path, receipt)
                status, _ = client.request(DATA_PATH, payload, method='PUT')
                if status != 202:
                    raise SubmissionError('Unexpected PUT response; reconcile before retrying.')
                wanted[patch['id']] = expected_row(by_id[patch['id']], patch)
                receipt['stage'] = f'read_back_row_{patch["id"]}'
                save(receipt_path, receipt)
                after = reader() if reader is not None else all_rows(client)
                actual = {r['id']: r for r in after}
                if actual != wanted:
                    raise SubmissionError('Read-back differs from the DOI-only expected table; reconcile before retrying.')
                receipt['confirmed_ids'].append(patch['id'])
                save(receipt_path, receipt)
            save(run / 'after.json', after)
            receipt.update(status='verified', verified_at=now(), after_rows=len(after),
                           non_doi_fields_unchanged=True, updates=len(pending))
            save(receipt_path, receipt)
            return receipt
        except Exception as error:
            receipt.update(status='failed_or_ambiguous', attention_required=True, failure_type=type(error).__name__)
            save(receipt_path, receipt)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username', default='yusriy')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--execute', action='store_true')
    mode.add_argument('--reconcile', action='store_true', help='Read-only comparison against the original backup; requires no password')
    args = parser.parse_args()
    try:
        plan = json.loads(PLAN.read_text())
        validate_plan(plan)
        if args.reconcile:
            result = reconcile(plan, RUN, fetch_rows())
        elif not args.execute:
            class PublicClient:
                def __init__(self): self.rows = fetch_rows()
                def request(self, path):
                    page = int(urllib.parse.parse_qs(urllib.parse.urlsplit(path).query)['page'][0])
                    return 200, self.rows[page*1000:(page+1)*1000]
            result = apply(PublicClient(), args.username, plan, RUN)
        else:
            if not sys.stdin.isatty():
                raise SubmissionError('Run --execute in an interactive local terminal; password entry must be hidden.')
            with warnings.catch_warnings():
                warnings.simplefilter('error', getpass.GetPassWarning)
                password = getpass.getpass('TIDBRepo password (hidden; not saved): ')
            client = Client(args.username, password)
            del password
            result = apply(client, args.username, plan, RUN, execute=True, reader=fetch_rows)
        print(json.dumps({k: result.get(k) for k in ('status', 'rows', 'updates', 'fields', 'after_rows', 'non_doi_fields_unchanged', 'completed_ids', 'pending_ids')}))
        return 0
    except (SubmissionError, ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1
    except (getpass.GetPassWarning, EOFError, KeyboardInterrupt):
        print('Cancelled or terminal cannot hide password; inspect receipt before retrying.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
