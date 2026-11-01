#!/usr/bin/env python3
"""Submit only the owner's three N02 coal factors; password stays in memory."""
import argparse
import fcntl
import getpass
import json
import math
import sys
import urllib.parse
import warnings
from pathlib import Path
from doi_identifiers import normalize_doi
from factor_plausibility import fetch_rows
from monthly_research import save, sha
from submit_r03 import Client, DATA_PATH, DATABASE, ROOT, SubmissionError, now

PLAN = ROOT / 'knowledge_base/reconciliations/reviews/2026-11-01-N02-upload.json'
RUN = ROOT / 'knowledge_base/literature_updates/runs/20261101-n02-upload'
DOI = '10.30880/ijie.2024.16.06.029'
FACTORS = [('Bituminous', .1011), ('Sub-Bituminous', .0883), ('Lignite', .0402)]


def validated_payload(plan):
    if plan.get('authorization', {}).get('tidbrepo_upload_authorized') is not True:
        raise SubmissionError('Explicit N02 upload authorization is required.')
    payload = plan.get('payload')
    expected = []
    for coal, value in FACTORS:
        expected.append({'countries':'Malaysia', 'sectors':'Energy',
            'category':'Fuel Combustion Activities - Electricity Generation',
            'condition':coal+' stationary combustion for electricity generation, Malaysia, 2019',
            'tier':2, 'min':None, 'max':None, 'median':None, 'mean':value,
            'stdev':None, 'scaling_factor':None, 'unit':'kg CH₄ TJ⁻¹',
            'url':'https://doi.org/'+DOI, 'doi_1':DOI})
    if plan.get('doi') != DOI or payload != expected:
        raise SubmissionError('Only the three exact approved N02 payloads may be submitted.')
    return payload


def same_record(row, payload):
    for key, value in payload.items():
        actual = row.get(key)
        if value is None:
            if actual not in (None, ''):
                return False
        elif key in ('mean', 'tier'):
            try:
                if not math.isclose(float(actual), float(value), rel_tol=1e-10, abs_tol=1e-12):
                    return False
            except (TypeError, ValueError):
                return False
        elif key.startswith('doi_'):
            if normalize_doi(actual) != value:
                return False
        elif str(actual).strip() != str(value).strip():
            return False
    return True


def source_rows(rows):
    return [r for r in rows if any(normalize_doi(r.get(f'doi_{i}')) == DOI for i in range(1,7))]


def submit(client, username, plan, run, execute=False, reader=fetch_rows):
    payload = validated_payload(plan)
    run.mkdir(parents=True, exist_ok=True)
    receipt_path = run/'receipt.json'
    with (run/'submission.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SubmissionError('Another N02 submission is active.') from None
        prior = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
        before = reader()
        old = {int(r['id']):r for r in before}
        if len(old) != len(before):
            raise SubmissionError('Duplicate record IDs; submission aborted.')
        sources = source_rows(before)
        exact = [[r for r in sources if same_record(r,p)] for p in payload]
        if len(sources)==3 and all(len(group)==1 for group in exact):
            result = {'status':'verified_existing','verified_at':now(), 'ids':[g[0]['id'] for g in exact],
                      'after_rows':len(before),'insert_performed_this_call':False,'previous_receipt':prior}
            save(receipt_path,result)
            return result
        if sources:
            raise SubmissionError('N02 DOI is partially present or differs; reconcile before submitting. No automatic retry.')
        if prior.get('status') in ('sending','failed_or_ambiguous','verified','verified_existing'):
            raise SubmissionError('An earlier N02 attempt requires reconciliation. No automatic retry.')
        # Same factor under a missing/different source merits manual reconciliation.
        for p in payload:
            for r in before:
                if (r.get('category')==p['category'] and r.get('unit')==p['unit']
                        and str(r.get('mean') or '')==str(p['mean'])):
                    raise SubmissionError('A matching category/unit/value already exists; check possible duplication.')
        if not execute:
            return {'status':'ready','before_rows':len(before),'new_records':3,'insert_performed_this_call':False}
        _, access = client.request(f'/api/v1/database/{DATABASE}/access/'+urllib.parse.quote(username,safe=''))
        if not isinstance(access,dict) or access.get('type') not in ('write_own','write_all'):
            raise SubmissionError('Account lacks database write access; no insert attempted.')
        if not (run/'before.json').exists():
            save(run/'before.json',before)
        receipt={'status':'sending','started_at':now(),'before_rows':len(before),
                 'confirmed_ids':[],'requests':[],'insert_performed_this_call':False}
        save(receipt_path,receipt)
        expected=dict(old)
        try:
            for p in payload:
                current=reader()
                if {int(r['id']):r for r in current} != expected:
                    raise SubmissionError('Live table changed during submission; stop and reconcile.')
                record={'id':max(expected,default=0)+1,**p}
                receipt['stage']='post_row_'+str(record['id'])
                receipt['requests'].append({'data':record})
                save(receipt_path,receipt)
                status,_ = client.request(DATA_PATH,{'data':record})
                receipt['insert_performed_this_call']=True
                receipt['last_http_status']=status
                save(receipt_path,receipt)
                if status!=201:
                    raise SubmissionError('Insert response was not HTTP 201; reconcile before retrying.')
                after=reader(); actual={int(r['id']):r for r in after}
                new=actual.get(record['id'])
                if (len(after)!=len(expected)+1 or not new or not same_record(new,p)
                        or any(actual.get(i)!=r for i,r in expected.items())):
                    raise SubmissionError('Public read-back failed or existing rows changed; stop and reconcile.')
                expected=actual
                receipt['confirmed_ids'].append(record['id'])
                save(receipt_path,receipt)
            save(run/'after.json',after)
            receipt.update(status='verified',verified_at=now(),after_rows=len(after),ids=receipt['confirmed_ids'])
            save(receipt_path,receipt)
            return receipt
        except Exception:
            receipt.update(status='failed_or_ambiguous',attention_required=True)
            save(receipt_path,receipt)
            raise


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username',default='yusriy')
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    try:
        plan=json.loads(PLAN.read_text()); validated_payload(plan)
        staging=ROOT/plan['source_staging']
        if sha(staging)!=plan['source_staging_sha256']:
            raise SubmissionError('Source staging changed; revalidate before submission.')
        client=None
        if args.execute:
            if not sys.stdin.isatty():
                raise SubmissionError('Run --execute in a local interactive terminal for hidden password entry.')
            with warnings.catch_warnings():
                warnings.simplefilter('error',getpass.GetPassWarning)
                password=getpass.getpass('TIDBRepo password (hidden; not saved): ')
            client=Client(args.username,password); del password
        result=submit(client,args.username,plan,RUN,args.execute)
        print(json.dumps({k:v for k,v in result.items() if k in ('status','before_rows','after_rows','new_records','ids')}))
        if args.execute: print('Local receipt:',RUN/'receipt.json')
        return 0
    except (SubmissionError,OSError,ValueError) as e:
        print(str(e),file=sys.stderr);return 1
    except (EOFError,KeyboardInterrupt,getpass.GetPassWarning):
        print('Interrupted or password entry unavailable; inspect the local receipt before retrying.',file=sys.stderr);return 1


if __name__=='__main__':
    raise SystemExit(main())
