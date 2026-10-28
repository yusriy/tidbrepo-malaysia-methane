import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
import submit_r03 as workflow


class FakeClient:
    def __init__(self, rows=None, access="write_own", fail_insert=False):
        self.rows = rows or []
        self.access = access
        self.fail_insert = fail_insert
        self.posts = []

    def request(self, path, data=None):
        if "/access/" in path:
            return 200, {"type": self.access}
        if data is not None:
            self.posts.append(copy.deepcopy(data))
            if self.fail_insert:
                raise workflow.SubmissionError("Ambiguous response")
            self.rows.append(copy.deepcopy(data["data"]))
            return 201, None
        return 200, copy.deepcopy(self.rows) if "page=0&" in path else []


class SubmissionTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads(workflow.PACKAGE.read_text())
        self.package.pop("upload_authorization_revoked", None)
        self.temp = tempfile.TemporaryDirectory()
        self.run = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_dry_run_checks_access_without_insert(self):
        client = FakeClient()
        result = workflow.submit(client, "yusriy", self.package, self.run)
        self.assertEqual(result["status"], "ready")
        self.assertEqual(client.posts, [])

    def test_insert_wraps_data_and_verifies_saved_values(self):
        old = {"id": 180, "mean": "1", "doi_1": "https://doi.org/other"}
        client = FakeClient([old])
        result = workflow.submit(client, "yusriy", self.package, self.run, True)
        self.assertEqual(result["status"], "verified")
        self.assertEqual(set(client.posts[0]), {"data"})
        self.assertEqual(result["row"]["id"], 181)
        self.assertEqual(result["row"]["mean"], 0.158)
        self.assertEqual(result["row"]["stdev"], 0.144)
        self.assertEqual(client.rows[0], old)

    def test_same_source_different_statistic_blocks_duplicate(self):
        row = {"id": 181, **self.package["payload"][0], "mean": 0.09}
        client = FakeClient([row])
        with self.assertRaisesRegex(workflow.SubmissionError, "already exists"):
            workflow.submit(client, "yusriy", self.package, self.run, True)
        self.assertEqual(client.posts, [])

    def test_already_saved_record_is_verified_without_second_insert(self):
        row = {"id": 181, **self.package["payload"][0]}
        client = FakeClient([row])
        result = workflow.submit(client, "yusriy", self.package, self.run, True)
        self.assertEqual(result["status"], "verified_existing")
        self.assertEqual(client.posts, [])

    def test_ambiguous_write_retains_receipt_and_blocks_retry(self):
        client = FakeClient(fail_insert=True)
        with self.assertRaises(workflow.SubmissionError):
            workflow.submit(client, "yusriy", self.package, self.run, True)
        receipt = json.loads((self.run / "api_submission_receipt.json").read_text())
        self.assertEqual(receipt["status"], "failed_or_ambiguous")
        with self.assertRaisesRegex(workflow.SubmissionError, "No automatic retry"):
            workflow.submit(client, "yusriy", self.package, self.run, True)
        self.assertEqual(len(client.posts), 1)

    def test_read_only_account_cannot_insert(self):
        client = FakeClient(access="read")
        with self.assertRaisesRegex(workflow.SubmissionError, "write access"):
            workflow.submit(client, "yusriy", self.package, self.run, True)
        self.assertEqual(client.posts, [])

    def test_permission_and_source_condition_are_required(self):
        for mutation in ["permission", "condition", "units"]:
            package = copy.deepcopy(self.package)
            if mutation == "permission":
                package["authorization"]["tidbrepo_upload_authorized"] = False
            elif mutation == "condition":
                package["payload"][0]["condition"] = "Forest"
            else:
                package["payload"][0]["unit"] = "g C m^-2 yr^-1"
            with self.subTest(mutation=mutation), self.assertRaises(workflow.SubmissionError):
                workflow.validated_payload(package)

    def test_revoked_permission_blocks_reinsertion(self):
        self.package["upload_authorization_revoked"] = True
        with self.assertRaisesRegex(workflow.SubmissionError, "revoked"):
            workflow.validated_payload(self.package)

    def test_credentials_are_not_forwarded_to_redirects(self):
        handler = workflow.NoRedirect()
        self.assertIsNone(handler.redirect_request(None, None, 302, "", {}, "https://other.invalid"))


if __name__ == "__main__":
    unittest.main()
