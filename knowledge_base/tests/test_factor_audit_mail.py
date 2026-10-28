import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

PIPELINE = Path(__file__).parents[1] / 'pipeline'
sys.path.insert(0, str(PIPELINE))
import factor_audit_mail as mail

class MailClaimTests(unittest.TestCase):
    def test_exclusive_claim_and_confirmed_receipt(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(mail, 'ROOT', Path(temp)):
            local = Path(temp) / 'knowledge_base/plausibility_audits/runs/run'
            local.mkdir(parents=True)
            report = Path(temp) / 'knowledge_base/reports/plausibility/run/report.html'
            report.parent.mkdir(parents=True)
            report.write_text('report')
            self.assertEqual(mail.claim('run')['status'], 'sending')
            with self.assertRaises(FileExistsError):
                mail.claim('run')
            with self.assertRaises(ValueError):
                mail.acknowledge('run', '')
            self.assertEqual(json.loads((local/'mail.json').read_text())['status'], 'sending')
            self.assertEqual(mail.acknowledge('run', 'gmail-confirmed-id')['status'], 'sent')
            with self.assertRaises(ValueError):
                mail.acknowledge('run', 'second-id')
