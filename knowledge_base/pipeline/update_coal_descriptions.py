#!/usr/bin/env python3
"""Owner-authorized description-only update of coal records 55 and 58."""
import argparse
import fcntl
import getpass
import json
import sys
import urllib.parse
import warnings
from pathlib import Path
from factor_plausibility import fetch_rows
from normalize_tidbrepo_dois import fingerprint
from submit_r03 import Client, DATABASE, DATA_PATH, ROOT, SubmissionError, now, save

PLAN = ROOT / 'knowledge_base/reconciliations/reviews/2026-10-29-coal-description-update.json'
RUN = ROOT / 'knowledge_base/literature_updates/runs/20261029-coal-descriptions'
DESCRIPTIONS = {
    55: 'Underground coal mining - IPCC Tier 1 low default',
    58: 'Surface coal mining - IPCC Tier 1 low default',
}


def validate_plan(plan):
    if plan.get('description_update_authorized') is not True:
        raise SubmissionError('Description-only authorization is required.')
    patches = plan.get('patches', [])
    if len(patches) != 2 or {p['id'] for p in patches} != set(DESCRIPTIONS):
        raise SubmissionError('Only rows 55 and 58 are authorized.')
    for patch in patches:
        if patch.get('after') != {'condition': DESCRIPTIONS[patch['id']]}:
            raise SubmissionError('Only the exact approved descriptions may change.')
        if set(patch.get('before', {})) != {'condition'}:
            raise SubmissionError('Only the condition column may change.')
    return patches


def apply(client, username, plan, run, execute=False, reader=fetch_rows):
    patches = validate_plan(plan)
    run.mkdir(parents=True, exist_ok=True)
    receipt_path = run / 'receipt.json'
    with (run / 'update.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        prior = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
        if prior.get('status') in ('sending', 'failed_or_ambiguous'):
            raise SubmissionError('Earlier attempt requires read-only reconciliation; do not retry automatically.')
        before = reader()
        by_id = {r['id']: r for r in before}
        if len(by_id) != len(before):
            raise SubmissionError('Duplicate record IDs; no update attempted.')
        pending = []
        for patch in patches:
            row = by_id.get(patch['id'])
            if row is None:
                raise SubmissionError('A target row is missing.')
            if row.get('condition') == patch['after']['condition']:
                expected_before = dict(row, condition=patch['before']['condition'])
                if fingerprint(expected_before) != patch['row_sha256']:
                    raise SubmissionError('A non-description target field changed; reconcile before proceeding.')
                continue
            if fingerprint(row) != patch['row_sha256']:
                raise SubmissionError('A target record changed since preflight; no update attempted.')
            pending.append(patch)
        if not pending:
            return {'status': 'verified_existing', 'rows': len(before), 'updates': 0}
        if not execute:
            return {'status': 'ready', 'rows': len(before), 'updates': len(pending)}
        _, access = client.request(f'/api/v1/database/{DATABASE}/access/' + urllib.parse.quote(username, safe=''))
        if not isinstance(access, dict) or access.get('type') not in ('write_own', 'write_all'):
            raise SubmissionError('Account lacks database write access.')
        if not (run / 'before.json').exists():
            save(run / 'before.json', before)
        receipt = {'status': 'sending', 'started_at': now(), 'confirmed_ids': [],
                   'before_rows': len(before), 'previous_receipt': prior}
        save(receipt_path, receipt)
        expected = dict(by_id)
        try:
            for patch in pending:
                row = by_id[patch['id']]
                # All keys protect the row identity and retained scientific fields;
                # only condition is present in data. Never POST or DELETE.
                payload = {'keys': {k: row[k] for k in ('id', 'condition', 'category', 'unit', 'min')},
                           'data': {'condition': DESCRIPTIONS[patch['id']]}}
                receipt['stage'] = f'write_row_{patch["id"]}'
                save(receipt_path, receipt)
                status, _ = client.request(DATA_PATH, payload, method='PUT')
                if status != 202:
                    raise SubmissionError('Unexpected update response; reconcile before retrying.')
                expected[patch['id']] = dict(row, **patch['after'])
                receipt['stage'] = f'read_back_row_{patch["id"]}'
                save(receipt_path, receipt)
                after = reader()
                actual = {r['id']: r for r in after}
                if actual != expected or len(after) != len(before):
                    raise SubmissionError('Table differs from description-only expected result; reconcile before retrying.')
                receipt['confirmed_ids'].append(patch['id'])
                save(receipt_path, receipt)
            save(run / 'after.json', after)
            receipt.update(status='verified', verified_at=now(), after_rows=len(after), updates=len(pending),
                           all_other_fields_unchanged=True)
            save(receipt_path, receipt)
            return receipt
        except Exception as error:
            receipt.update(status='failed_or_ambiguous', attention_required=True, failure_type=type(error).__name__)
            save(receipt_path, receipt)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username', default='yusriy')
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    try:
        plan = json.loads(PLAN.read_text())
        validate_plan(plan)
        client = None
        if args.execute:
            if not sys.stdin.isatty():
                raise SubmissionError('Run --execute in an interactive local terminal for hidden password entry.')
            with warnings.catch_warnings():
                warnings.simplefilter('error', getpass.GetPassWarning)
                password = getpass.getpass('TIDBRepo password (hidden; not saved): ')
            client = Client(args.username, password)
            del password
        result = apply(client, args.username, plan, RUN, args.execute)
        print(json.dumps({k: result.get(k) for k in ('status', 'rows', 'updates', 'after_rows', 'all_other_fields_unchanged')}))
        return 0
    except (SubmissionError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    except (EOFError, KeyboardInterrupt, getpass.GetPassWarning):
        print('Cancelled or terminal cannot hide the password; inspect receipt before retrying.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
