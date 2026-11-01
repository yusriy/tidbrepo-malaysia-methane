import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).parents[1]/'pipeline'))
import update_coal_descriptions as m

class CoalDescriptionTests(unittest.TestCase):
    def setUp(self):
        self.rows=[dict(id=i,condition='Mining',category='Underground',unit='kg CH4 TJ-1',min=v) for i,v in ((55,'10'),(58,'0.3'))]
        self.plan={'description_update_authorized':True,'patches':[{'id':r['id'],'before':{'condition':'Mining'},'after':{'condition':m.DESCRIPTIONS[r['id']]},'row_sha256':m.fingerprint(r)} for r in self.rows]}

    def client(self, ambiguous=False):
        rows=self.rows
        class Fake:
            writes=[]
            def request(self,path,data=None,method=None):
                if '/access/' in path:return 200,{'type':'write_all'}
                self.writes.append(data)
                if ambiguous:raise m.SubmissionError('HTTP 401')
                assert method=='PUT'
                next(r for r in rows if r['id']==data['keys']['id']).update(data['data'])
                return 202,None
        return Fake()

    def test_only_descriptions_change_and_repeat_is_idempotent(self):
        client=self.client()
        with tempfile.TemporaryDirectory() as temp:
            r=m.apply(client,'owner',self.plan,Path(temp),True,reader=lambda:json.loads(json.dumps(self.rows)))
            self.assertTrue(r['all_other_fields_unchanged'])
            self.assertEqual([r['min'] for r in self.rows],['10','0.3'])
            self.assertTrue(all(r['unit']=='kg CH4 TJ-1' and r['category']=='Underground' for r in self.rows))
            self.assertTrue(all(set(p['data'])=={'condition'} for p in client.writes))
            self.assertEqual(m.apply(client,'owner',self.plan,Path(temp),True,reader=lambda:self.rows)['updates'],0)

    def test_plan_cannot_change_units_or_target_extra_rows(self):
        self.plan['patches'][0]['after']['unit']='other'
        with self.assertRaises(m.SubmissionError):m.validate_plan(self.plan)
        self.plan['patches'][0]['after']={'condition':m.DESCRIPTIONS[55]}
        self.plan['patches'][0]['id']=181
        with self.assertRaises(m.SubmissionError):m.validate_plan(self.plan)

    def test_stale_numeric_value_stops_before_write(self):
        client=self.client();self.rows[0]['min']='11'
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(m.SubmissionError):m.apply(client,'owner',self.plan,Path(temp),True,reader=lambda:self.rows)
            self.assertEqual(len(client.writes),0)

    def test_ambiguous_attempt_cannot_retry(self):
        client=self.client(ambiguous=True)
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(m.SubmissionError):m.apply(client,'owner',self.plan,Path(temp),True,reader=lambda:self.rows)
            with self.assertRaises(m.SubmissionError):m.apply(client,'owner',self.plan,Path(temp),True,reader=lambda:self.rows)
            self.assertEqual(len(client.writes),1)
