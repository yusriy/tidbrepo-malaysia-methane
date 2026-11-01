import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pipeline'))
import submit_n02 as w

class FakeClient:
    def __init__(self, fail_at=None, access='write_own'):
        self.rows=[{'id':180,'mean':'1','unit':'kg CH₄ TJ⁻¹','category':'Other','doi_1':'10.1234/old'}]
        self.posts=[];self.fail_at=fail_at;self.access=access
    def read(self):return copy.deepcopy(self.rows)
    def request(self,path,data=None):
        if '/access/' in path:return 200,{'type':self.access}
        self.posts.append(copy.deepcopy(data))
        if len(self.posts)==self.fail_at:raise w.SubmissionError('Simulated ambiguous response')
        self.rows.append(copy.deepcopy(data['data']))
        return 201,None

class N02SubmissionTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads(w.PLAN.read_text());self.tmp=tempfile.TemporaryDirectory();self.run=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def test_dry_run_never_posts(self):
        c=FakeClient();r=w.submit(None,'yusriy',self.plan,self.run,False,c.read)
        self.assertEqual(r['new_records'],3);self.assertFalse(c.posts)
    def test_three_exact_inserts_readback_and_existing_rows_preserved(self):
        c=FakeClient();old=c.read();r=w.submit(c,'yusriy',self.plan,self.run,True,c.read)
        self.assertEqual(r['status'],'verified');self.assertEqual(r['ids'],[181,182,183]);self.assertEqual(c.rows[:1],old)
        self.assertEqual([p['data']['mean'] for p in c.posts],[.1011,.0883,.0402]);self.assertEqual(len(c.posts),3)
        self.assertTrue(all(p['data']['stdev'] is None for p in c.posts))
    def test_no_reinsertion_of_three_exact_existing_records(self):
        c=FakeClient();w.submit(c,'yusriy',self.plan,self.run,True,c.read)
        r=w.submit(c,'yusriy',self.plan,self.run,True,c.read)
        self.assertEqual(r['status'],'verified_existing');self.assertEqual(len(c.posts),3)
    def test_partial_failure_stops_and_no_blind_retry(self):
        c=FakeClient(fail_at=2)
        with self.assertRaises(w.SubmissionError):w.submit(c,'yusriy',self.plan,self.run,True,c.read)
        r=json.loads((self.run/'receipt.json').read_text());self.assertEqual(r['status'],'failed_or_ambiguous');self.assertEqual(r['confirmed_ids'],[181])
        with self.assertRaisesRegex(w.SubmissionError,'No automatic retry'):w.submit(c,'yusriy',self.plan,self.run,True,c.read)
        self.assertEqual(len(c.posts),2)
    def test_read_only_access_never_posts(self):
        c=FakeClient(access='read')
        with self.assertRaisesRegex(w.SubmissionError,'write access'):w.submit(c,'yusriy',self.plan,self.run,True,c.read)
        self.assertFalse(c.posts)
    def test_whitelist_and_authorization_reject_changes(self):
        for key in ['mean','unit','condition','tier','extra','authorization']:
            p=copy.deepcopy(self.plan)
            if key=='authorization':p['authorization']['tidbrepo_upload_authorized']=False
            elif key=='extra':p['payload'].append(copy.deepcopy(p['payload'][0]))
            else:p['payload'][0][key]='changed'
            with self.subTest(key=key),self.assertRaises(w.SubmissionError):w.validated_payload(p)
    def test_similar_source_but_wrong_value_blocks_all_inserts(self):
        c=FakeClient();r=copy.deepcopy(self.plan['payload'][0]);r.update(id=181,mean=.2);c.rows.append(r)
        with self.assertRaises(w.SubmissionError):w.submit(c,'yusriy',self.plan,self.run,True,c.read)
        self.assertFalse(c.posts)
    def test_unrelated_change_during_readback_is_detected(self):
        c=FakeClient();read_count=0
        def reader():
            nonlocal read_count
            read_count+=1
            if read_count==3:c.rows[0]['mean']='2'
            return c.read()
        with self.assertRaisesRegex(w.SubmissionError,'existing rows changed'):w.submit(c,'yusriy',self.plan,self.run,True,reader)
        self.assertEqual(len(c.posts),1)
