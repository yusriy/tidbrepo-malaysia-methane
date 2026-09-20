import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "pipeline"))
import tidbrepo_literature_update as workflow


CONFIG = json.loads((PACKAGE_ROOT / "config" / "tidbrepo_literature_update.json").read_text())


class ScreeningTests(unittest.TestCase):
    def test_malaysian_numeric_methane_study_scores_high(self):
        score, flags = workflow.screening_score(
            "Methane flux from rice in Malaysia",
            "Measured CH4 emission factor was 1.80 kg CH4 ha-1 day-1.",
            CONFIG,
        )
        self.assertGreaterEqual(score, CONFIG["minimum_screening_score"])
        self.assertIn("malaysia_context", flags)
        self.assertIn("numeric_value_in_abstract", flags)

    def test_non_malaysian_review_is_not_eligible(self):
        score, flags = workflow.screening_score(
            "A global review of methane methods",
            "We review methane monitoring worldwide.",
            CONFIG,
        )
        self.assertLess(score, CONFIG["minimum_screening_score"])
        self.assertIn("likely_secondary_source", flags)

    def test_methane_measurement_without_malaysia_lacks_mandatory_flag(self):
        score, flags = workflow.screening_score(
            "Methane flux from a European wetland",
            "The measured methane flux was 2.3 kg CH4 ha-1 year-1.",
            CONFIG,
        )
        self.assertGreater(score, 0)
        self.assertNotIn("malaysia_context", flags)

    def test_malaysian_affiliation_signal(self):
        work = {"authorships": [{"institutions": [{"country_code": "MY"}]}]}
        self.assertTrue(workflow.has_malaysian_affiliation(work))

    def test_prior_run_candidates_are_part_of_seen_identity_set(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            runs = root / "runs"
            run = runs / "previous"
            run.mkdir(parents=True)
            (run / "candidates.jsonl").write_text(
                json.dumps({
                    "doi": "10.1234/example",
                    "openalex_id": "https://openalex.org/W123",
                    "title": "A Malaysian Methane Paper",
                }) + "\n",
                encoding="utf-8",
            )
            dois, openalex_ids, titles = workflow.existing_candidate_identities(
                root / "missing.sqlite", root / "missing.json", runs
            )
            self.assertIn("10.1234/example", dois)
            self.assertIn("https://openalex.org/W123", openalex_ids)
            self.assertIn("a malaysian methane paper", titles)


class ExtractionTests(unittest.TestCase):
    def test_exact_value_and_unit_are_retained(self):
        text = "The Malaysian system achieved a methane yield of 0.218 ± 0.032 L CH4/g COD removed."
        matches = list(workflow.evidence_sentences(text))
        self.assertEqual(len(matches), 1)
        _, match = matches[0]
        self.assertIn("0.218", match.group(0))
        self.assertIn("L CH4/g COD removed", match.group(0))

    def test_pdf_line_numbers_are_not_misread_as_units(self):
        noisy = (
            "In the 210laboratory, CH4 concentration was measured and "
            "the 212gas flux was calculated from 2010 to 2013."
        )
        self.assertEqual(list(workflow.evidence_sentences(noisy)), [])


class ApprovalGateTests(unittest.TestCase):
    def test_prepare_upload_rejects_incomplete_approved_row(self):
        with tempfile.TemporaryDirectory() as temp:
            review = Path(temp) / "review.csv"
            with review.open("w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.DictWriter(handle, fieldnames=workflow.REVIEW_FIELDS)
                writer.writeheader()
                writer.writerow({"proposal_id": "p1", "decision": "approve", "countries": "Malaysia"})
            args = type("Args", (), {"review_csv": review, "output": None})()
            self.assertEqual(workflow.command_prepare_upload(args), 1)

    def test_upload_is_dry_run_by_default(self):
        with tempfile.TemporaryDirectory() as temp:
            payload = Path(temp) / "payload.json"
            payload.write_text("[]", encoding="utf-8")
            args = type("Args", (), {
                "payload": payload, "execute": False, "confirm": "", "endpoint": "https://example.invalid",
                "token_env": "TIDBREPO_API_TOKEN",
            })()
            self.assertEqual(workflow.command_upload(args), 0)


if __name__ == "__main__":
    unittest.main()
