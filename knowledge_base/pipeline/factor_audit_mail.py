#!/usr/bin/env python3
"""Local, exclusive mail claims. Never sends mail or stores credentials."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from factor_plausibility import ROOT


def claim(run_id):
    directory = ROOT / 'knowledge_base/plausibility_audits/runs' / run_id
    report = ROOT / 'knowledge_base/reports/plausibility' / run_id / 'report.html'
    if not directory.is_dir() or not report.is_file():
        raise ValueError('Report and local snapshot required before claiming')
    state = {'run_id': run_id, 'status': 'sending', 'recipient': 'yusriy@usm.my',
             'sender': 'admin.atmosfera@gmail.com', 'claimed_at': datetime.now(timezone.utc).isoformat(),
             'report_sha256': hashlib.sha256(report.read_bytes()).hexdigest()}
    with (directory / 'mail.json').open('x') as stream:
        json.dump(state, stream, indent=2)
    return state


def acknowledge(run_id, message_id):
    if not message_id or not message_id.strip():
        raise ValueError('Confirmed Gmail message ID is required')
    path = ROOT / 'knowledge_base/plausibility_audits/runs' / run_id / 'mail.json'
    state = json.loads(path.read_text())
    if state['status'] != 'sending':
        raise ValueError('Mail is not awaiting acknowledgement')
    state.update(status='sent', message_id=message_id, sent_at=datetime.now(timezone.utc).isoformat())
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(state, indent=2) + '\n')
    temporary.replace(path)
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['claim', 'ack'])
    parser.add_argument('run_id')
    parser.add_argument('--message-id')
    args = parser.parse_args()
    if not args.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.run_id):
        parser.error('Invalid run ID')
    print(json.dumps(claim(args.run_id) if args.action == 'claim' else acknowledge(args.run_id, args.message_id)))


if __name__ == '__main__':
    main()
