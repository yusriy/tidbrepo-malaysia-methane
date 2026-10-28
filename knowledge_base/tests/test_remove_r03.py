import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
import remove_r03 as workflow


class FakeClient:
    def __init__(self, rows, access="write_own", ambiguous=False):
        self.rows = copy.deepcopy(rows)
        self.access = access
        self.ambiguous = ambiguous
        self.deletes = []

    def request(self, path, data=None, method=None):
        if "/access/" in path:
            return 200, {"type": self.access}
        if method == "DELETE":
            self.deletes.append(copy.deepcopy(data))
            if self.ambiguous:
                raise workflow.SubmissionError("Ambiguous response")
            self.rows = [r for r in self.rows if int(r["id"]) != data["keys"]["id"]]
            return 202, None
        return 200, copy.deepcopy(self.rows) if "page=0&" in path else []


class RemovalTests(unittest.TestCase):
    def setUp(self):
        self.authorization = json.loads(workflow.AUTHORIZATION.read_text())
        self.row = self.authorization["expected_row"]
        self.other = {"id": 180, "mean": "1.23", "doi_1": "other"}
        self.temp = tempfile.TemporaryDirectory()
        self.run = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_only_target_id_and_doi_are_deleted_and_other_rows_preserved(self):
        client = FakeClient([self.other, self.row])
        result = workflow.remove(client, "yusriy", self.authorization, self.run, True)
        self.assertEqual(client.deletes, [{"keys": {"id": 181, "doi_1": self.row["doi_1"]}}])
        self.assertEqual(result["status"], "verified_removed")
        self.assertTrue(result["all_other_rows_unchanged"])
        self.assertEqual(client.rows, [self.other])
        self.assertEqual(json.loads((self.run / "authenticated-before.json").read_text()), [self.other, self.row])

    def test_changed_record_is_not_deleted(self):
        changed = {**self.row, "mean": "999"}
        client = FakeClient([self.other, changed])
        with self.assertRaisesRegex(workflow.SubmissionError, "differs"):
            workflow.remove(client, "yusriy", self.authorization, self.run, True)
        self.assertEqual(client.deletes, [])

    def test_absent_record_is_confirmed_without_deletion(self):
        client = FakeClient([self.other])
        result = workflow.remove(client, "yusriy", self.authorization, self.run, True)
        self.assertEqual(result["status"], "verified_absent")
        self.assertEqual(client.deletes, [])

    def test_dry_run_does_not_delete(self):
        client = FakeClient([self.row])
        self.assertEqual(workflow.remove(client, "yusriy", self.authorization, self.run)["status"], "ready")
        self.assertEqual(client.deletes, [])

    def test_ambiguous_request_blocks_blind_retry(self):
        client = FakeClient([self.row], ambiguous=True)
        with self.assertRaises(workflow.SubmissionError):
            workflow.remove(client, "yusriy", self.authorization, self.run, True)
        with self.assertRaisesRegex(workflow.SubmissionError, "no automatic retry"):
            workflow.remove(client, "yusriy", self.authorization, self.run, True)
        self.assertEqual(len(client.deletes), 1)

    def test_authorization_and_existing_write_access_are_required(self):
        client = FakeClient([self.row], access="read")
        with self.assertRaisesRegex(workflow.SubmissionError, "write access"):
            workflow.remove(client, "yusriy", self.authorization, self.run, True)
        self.assertEqual(client.deletes, [])
        denied = {**self.authorization, "deletion_authorized": False}
        with self.assertRaisesRegex(workflow.SubmissionError, "authorization"):
            workflow.remove(FakeClient([self.row]), "yusriy", denied, self.run, True)


if __name__ == "__main__":
    unittest.main()
