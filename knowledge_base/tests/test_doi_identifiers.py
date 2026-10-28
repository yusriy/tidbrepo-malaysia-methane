import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).parents[1] / 'pipeline'))
from doi_identifiers import normalize_doi, validated_doi, doi_url
from factor_plausibility import prepare
import normalize_tidbrepo_dois as update

class DoiTests(unittest.TestCase):
    def test_canonical_forms_and_safe_links(self):
        for value in ('10.1234/ABC', ' https://doi.org/10.1234/ABC ', 'http://dx.doi.org/10.1234/ABC', 'doi:10.1234/ABC'):
            self.assertEqual(validated_doi(value), '10.1234/abc')
            self.assertEqual(doi_url(value), 'https://doi.org/10.1234/abc')
        self.assertEqual(normalize_doi('https://doi.org/10.1234%2FABC'), '10.1234/abc')
        with self.assertRaises(ValueError): validated_doi('https://evil.example/10.1234/abc')

    def test_shared_source_identity_retains_original(self):
        original = 'https://doi.org/10.1234/ABC'
        r=prepare({'id':1, 'unit':'u', 'doi_1':original, 'doi_2':'10.1234/abc'})
        self.assertEqual(r['dois'], ['10.1234/abc'])
        self.assertEqual(r['reported_dois']['doi_1'], original)

    def test_owner_default_convention_only_for_ipcc_min_only(self):
        r=prepare({'id':1,'countries':'IPCC','min':'10','unit':'u'})
        self.assertEqual(r['comparison_values']['default_factor'],10)
        self.assertNotIn('min',r['comparison_values'])
        self.assertEqual(r['reported_values']['min'],'10')
        self.assertEqual(prepare({'id':2,'countries':'Malaysia','min':'10','unit':'u'})['comparison_values']['min'],10)
        self.assertIsNone(prepare({'id':3,'countries':'IPCC','min':'1','max':'10','unit':'u'})['comparison_values']['default_factor'])

class DoiUpdateTests(unittest.TestCase):
    def setUp(self):
        self.row={'id':1,'doi_1':'https://doi.org/10.1234/ABC','mean':'2','unit':'u'}
        self.patch={'id':1,'before':{'doi_1':self.row['doi_1']},'after':{'doi_1':'10.1234/abc'},'row_sha256':update.fingerprint(self.row)}
        self.plan={'doi_format_update_authorized':True,'canonical_format':'lowercase bare DOI','patches':[self.patch]}

    def test_plan_rejects_non_doi_and_identity_changes(self):
        update.validate_plan(self.plan)
        self.patch['after']['doi_1']='10.1234/different'
        with self.assertRaises(update.SubmissionError): update.validate_plan(self.plan)
        self.patch['after']={'unit':'other'}
        with self.assertRaises(update.SubmissionError): update.validate_plan(self.plan)

    def client(self, ambiguous=False):
        outer=self
        class Fake:
            def __init__(self): self.rows=[dict(outer.row)];self.writes=0
            def request(self,path,data=None,method=None):
                if '/access/' in path:return 200,{'type':'write_all'}
                if method=='PUT':
                    self.writes+=1
                    self.rows[0].update(data['data'])
                    if ambiguous:raise update.SubmissionError('ambiguous')
                    return 202,None
                page=int(update.urllib.parse.parse_qs(update.urllib.parse.urlsplit(path).query)['page'][0])
                return 200,self.rows if page==0 else []
        return Fake()

    def test_scoped_put_and_idempotence(self):
        c=self.client()
        with tempfile.TemporaryDirectory() as temp:
            r=update.apply(c,'owner',self.plan,Path(temp),True)
            self.assertTrue(r['non_doi_fields_unchanged'])
            self.assertEqual(c.rows[0]['mean'],'2')
            self.assertEqual(update.apply(c,'owner',self.plan,Path(temp),True)['updates'],0)
            self.assertEqual(c.writes,1)

    def test_stale_row_and_ambiguous_attempt_stop(self):
        c=self.client();c.rows[0]['mean']='3'
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(update.SubmissionError):update.apply(c,'owner',self.plan,Path(temp),True)
            self.assertEqual(c.writes,0)
        c=self.client(ambiguous=True)
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(update.SubmissionError):update.apply(c,'owner',self.plan,Path(temp),True)
            with self.assertRaises(update.SubmissionError):update.apply(c,'owner',self.plan,Path(temp),True)
            self.assertEqual(c.writes,1)

    def test_public_reader_and_reconciled_resume_preserve_history(self):
        c=self.client(ambiguous=True)
        with tempfile.TemporaryDirectory() as temp:
            run=Path(temp)
            with self.assertRaises(update.SubmissionError):
                update.apply(c,'owner',self.plan,run,True)
            # The simulated PUT applied but its response was ambiguous. Read-only
            # reconciliation establishes the actual state without another PUT.
            receipt=update.reconcile(self.plan,run,[dict(x) for x in c.rows])
            self.assertEqual(receipt['status'],'verified')
            self.assertEqual(receipt['previous_receipt']['status'],'failed_or_ambiguous')
            self.assertEqual(c.writes,1)
            self.assertEqual(update.apply(c,'owner',self.plan,run,True)['updates'],0)

    def test_reconciliation_refuses_unrelated_changes(self):
        c=self.client(ambiguous=True)
        with tempfile.TemporaryDirectory() as temp:
            run=Path(temp)
            with self.assertRaises(update.SubmissionError):update.apply(c,'owner',self.plan,run,True)
            c.rows[0]['mean']='99'
            with self.assertRaises(update.SubmissionError):update.reconcile(self.plan,run,c.rows)
            self.assertEqual(json.loads((run/'receipt.json').read_text())['status'],'failed_or_ambiguous')

    def test_execute_can_use_public_readback_only(self):
        c=self.client()
        original=c.request
        def authenticated(path,data=None,method=None):
            if method!='PUT' and '/access/' not in path:
                self.fail('Table reads must use injected public reader')
            return original(path,data,method)
        c.request=authenticated
        with tempfile.TemporaryDirectory() as temp:
            r=update.apply(c,'owner',self.plan,Path(temp),True,reader=lambda:[dict(x) for x in c.rows])
            self.assertEqual(r['status'],'verified')

class UploadDoiTests(unittest.TestCase):
    def test_future_upload_has_canonical_doi_and_original_provenance(self):
        import csv
        from types import SimpleNamespace
        import tidbrepo_literature_update as workflow
        with tempfile.TemporaryDirectory() as temp:
            review=Path(temp)/'review.csv';output=Path(temp)/'approved.json'
            row={k:'' for k in workflow.REVIEW_FIELDS}
            row.update(proposal_id='p',decision='approve',countries='Malaysia',sectors='AFOLU',category='Peat lands',condition='Forest',tier='2',unit='kg CH4 ha-1 day-1',mean='1',url='https://doi.org/10.1234/ABC',doi_1='https://doi.org/10.1234/ABC')
            with review.open('w') as f:
                writer=csv.DictWriter(f,fieldnames=workflow.REVIEW_FIELDS);writer.writeheader();writer.writerow(row)
            self.assertEqual(workflow.command_prepare_upload(SimpleNamespace(review_csv=review,output=output)),0)
            self.assertEqual(json.loads(output.read_text())[0]['doi_1'],'10.1234/abc')
            provenance=json.loads(output.with_name('approved_provenance.json').read_text())[0]
            self.assertEqual(provenance['reported_doi'],row['doi_1'])
