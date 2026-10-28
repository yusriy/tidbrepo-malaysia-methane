import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
import monthly_research as monthly
import tidbrepo_literature_update as literature


def fixture(repo, run_id="20261001T000000Z", proposals=True):
    run = repo / monthly.RUNS / run_id
    run.mkdir(parents=True, exist_ok=True)
    monthly.save(run / "manifest.json", {"run_id": run_id, "works_deduplicated": 903, "candidates_retained": 1})
    literature.write_jsonl(run / "candidates.jsonl", [{
        "candidate_id": "candidate_a", "doi": "10.1234/example", "title": "Malaysian methane flux",
        "source_url": "https://example.org/paper", "screening_score": 6,
        "discovered_by": "OpenAlex API", "discovered_at": "2026-10-01T00:00:00+00:00",
    }])
    if proposals:
        literature.write_jsonl(run / "proposals.jsonl", [{
            "proposal_id": "proposal_a", "candidate_id": "candidate_a", "doi": "10.1234/example",
            "source_url": "https://example.org/paper", "pdf_sha256": "a" * 64, "page": 2,
            "evidence_quote": "The measured methane flux was 1.8 kg CH4 ha-1 day-1.",
            "raw_value_text": "1.8 kg CH4 ha-1 day-1", "unit_original": "kg CH4 ha-1 day-1",
            "verification_status": "verified",  # An upstream assertion cannot promote evidence.
            "provenance_chain": [{"stage": "evidence", "page": 2}],
        }])
    return run


class QueueTests(unittest.TestCase):
    def test_queue_preserves_evidence_and_forces_unverified(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            run = fixture(repo)
            record = monthly.build_curated(run)
            files = monthly.publish_queue(repo, record)
            result = monthly.validate_wiki(repo)
            self.assertEqual(result["broken_wikilinks"], 0)
            curated = monthly.load(repo / files[0])
            self.assertEqual(curated["verification_status"], "unverified")
            proposal = curated["proposals"][0]
            self.assertEqual(proposal["verification_status"], "proposed_human_review")
            for key in ("doi", "source_url", "evidence_quote", "unit_original", "pdf_sha256", "page", "provenance_chain"):
                self.assertEqual(proposal[key], record["proposals"][0][key])
            before = (repo / files[1]).read_bytes()
            monthly.publish_queue(repo, record)
            self.assertEqual((repo / files[1]).read_bytes(), before)
            record["proposals"][0]["page"] = 3
            with self.assertRaisesRegex(ValueError, "different evidence"):
                monthly.publish_queue(repo, record)

    def test_wiki_validator_rejects_missing_link_and_promoted_measurement(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            run = fixture(repo)
            record = monthly.build_curated(run)
            files = monthly.publish_queue(repo, record)
            record["proposals"][0]["verification_status"] = "verified"
            monthly.save(repo / files[0], record)
            (repo / files[1]).write_text("[[missing-paper]]")
            with self.assertRaisesRegex(ValueError, "Wiki validation failed") as caught:
                monthly.validate_wiki(repo)
            self.assertIn("missing-paper", str(caught.exception))
            self.assertIn("without scientific review", str(caught.exception))

    def test_partial_extraction_failure_still_queues_discovery(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            def fake_stage(args, **kwargs):
                if "discover" in args:
                    fixture(repo, proposals=False)
                elif "extract" in args:
                    raise subprocess.CalledProcessError(1, args)
            with patch.object(monthly.subprocess, "run", side_effect=fake_stage), patch.object(monthly, "sync_github", return_value={"status": "pushed"}) as sync:
                rc = monthly.run_monthly(repo, sys.executable, "20261001T000000Z", True)
            self.assertEqual(rc, 1)
            self.assertEqual(sync.call_args.args[2]["candidates"][0]["candidate_id"], "candidate_a")
            summary = monthly.load(repo / monthly.RUNS / "20261001T000000Z/run_summary.json")
            self.assertEqual(summary["failed_stage"], "extraction")
            self.assertIsNone(summary["methane_measurements_proposed"])

    def test_successful_run_records_counts_and_all_stages(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            def fake_stage(args, **kwargs):
                if "discover" in args:
                    fixture(repo)
            with patch.object(monthly.subprocess, "run", side_effect=fake_stage), patch.object(monthly, "sync_github", return_value={"status": "pushed"}):
                rc = monthly.run_monthly(repo, sys.executable, "20261001T000000Z", True)
            self.assertEqual(rc, 0)
            summary = monthly.load(repo / monthly.RUNS / "20261001T000000Z/run_summary.json")
            self.assertEqual(summary["status"], "succeeded")
            self.assertEqual(summary["stages"], dict.fromkeys(("discovery", "extraction", "review"), "succeeded"))
            self.assertEqual(summary["methane_measurements_proposed"], 1)


class NotificationTests(unittest.TestCase):
    def test_summary_counts_and_delivery_receipt(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            run = fixture(repo)
            summary = monthly.write_notification(repo, run, {"status": "succeeded"})
            self.assertEqual(summary["publications_screened"], 903)
            self.assertEqual(summary["new_candidate_papers"], 1)
            self.assertEqual(summary["methane_measurements_proposed"], 1)
            self.assertEqual(len(summary["papers_requiring_manual_review"]), 1)
            self.assertEqual(len(monthly.pending_notifications(repo)), 1)
            monthly.delivery_update(repo, run.name, "claim")
            self.assertEqual(monthly.pending_notifications(repo), [])
            with self.assertRaises(ValueError):
                monthly.delivery_update(repo, run.name, "claim")
            monthly.delivery_update(repo, run.name, "ack", "gmail-confirmed-id")
            self.assertEqual(monthly.pending_notifications(repo), [])
            monthly.write_notification(repo, run, {"status": "succeeded"})
            self.assertEqual(monthly.pending_notifications(repo), [])

    def test_failed_discovery_uses_unknown_counts_and_no_publication(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            with patch.object(monthly.subprocess, "run", side_effect=subprocess.CalledProcessError(1, ["discover"])), patch.object(monthly, "sync_github") as sync:
                self.assertEqual(monthly.run_monthly(repo, sys.executable, "failed_discovery", True), 1)
            sync.assert_not_called()
            summary = monthly.load(repo / monthly.RUNS / "failed_discovery/run_summary.json")
            self.assertEqual(summary["status"], "failed")
            self.assertIsNone(summary["publications_screened"])
            self.assertIn("unavailable", monthly.render_summary(summary))
            self.assertEqual(len(monthly.pending_notifications(repo)), 1)

    def test_hard_killed_run_is_recovered_after_timeout(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            run = fixture(repo, proposals=False)
            monthly.save(run / "run_status.json", {"status": "running", "active_stage": "extraction",
                "started_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()})
            notifications = monthly.pending_notifications(repo)
            self.assertEqual(notifications[0]["summary"]["status"], "failed")
            self.assertEqual(notifications[0]["summary"]["failure_type"], "InterruptedRun")

    def test_run_id_cannot_escape_archive_and_existing_run_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            run = fixture(repo)
            with self.assertRaises(ValueError):
                monthly.run_monthly(repo, sys.executable, "../escape", False)
            before = (run / "manifest.json").read_bytes()
            with self.assertRaises(ValueError):
                monthly.run_monthly(repo, sys.executable, run.name, False)
            self.assertEqual((run / "manifest.json").read_bytes(), before)


class GitPublicationTests(unittest.TestCase):
    def test_failed_tests_prevent_commit_and_push(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            run = fixture(repo)
            calls = []
            def fake_command(args, cwd, **kwargs):
                calls.append(args)
                if args[:3] == ["git", "worktree", "add"]:
                    (repo / monthly.STATE / "github-review").mkdir(parents=True)
                if args[:3] == ["git", "branch", "--show-current"]:
                    return monthly.BRANCH
                if "unittest" in args:
                    raise subprocess.CalledProcessError(1, args, output="simulated failing test")
                return ""
            with patch.object(monthly, "command", side_effect=fake_command), patch.object(monthly.subprocess, "run"):
                with self.assertRaises(subprocess.CalledProcessError):
                    monthly.sync_github(repo, run, monthly.build_curated(run), sys.executable)
            self.assertFalse(any(args[:2] in (["git", "commit"], ["git", "push"]) for args in calls))
            self.assertIn("simulated failing test", (run / "publication_tests.log").read_text())

    def test_real_git_publication_isolated_and_excludes_raw_and_pdf(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo"
            remote = root / "remote.git"
            repo.mkdir()
            def git(*args, cwd=repo):
                return monthly.command(["git", *args], cwd)
            git("init", "-b", "main")
            git("config", "user.name", "Test Researcher")
            git("config", "user.email", "test@example.invalid")
            (repo / ".gitignore").write_text("knowledge_base/literature_updates/state/\nknowledge_base/literature_updates/runs/\n")
            tests = repo / "knowledge_base/tests"
            tests.mkdir(parents=True)
            (tests / "test_smoke.py").write_text("import unittest\nclass Smoke(unittest.TestCase):\n def test_ok(self): self.assertTrue(True)\n")
            git("add", ".")
            git("commit", "-m", "baseline")
            baseline = git("rev-parse", "HEAD")
            git("init", "--bare", str(remote))
            git("remote", "add", "origin", str(remote))
            run = fixture(repo)
            (run / "private.pdf").write_bytes(b"PDF local only")
            (run / "raw.json").write_text("private raw response")
            (repo / "unrelated.txt").write_text("uncommitted human work")
            result = monthly.sync_github(repo, run, monthly.build_curated(run), sys.executable)
            self.assertEqual(result["status"], "pushed")
            self.assertEqual(git("branch", "--show-current"), "main")
            self.assertEqual(git("rev-parse", "HEAD"), baseline)
            tree = git("ls-tree", "-r", "--name-only", monthly.BRANCH)
            self.assertNotIn("private.pdf", tree)
            self.assertNotIn("raw.json", tree)
            self.assertNotIn("unrelated.txt", tree)
            self.assertIn("curated/" + run.name + ".json", tree)
            self.assertTrue((run / "wiki_validation.json").exists())
            self.assertTrue((run / "publication_tests.log").exists())
            # An unchanged retry pushes safely without another commit.
            retry = monthly.sync_github(repo, run, monthly.build_curated(run), sys.executable)
            self.assertEqual(retry["commit"], result["commit"])

    def test_wiki_failure_prevents_commit_and_push(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            run = fixture(repo)
            calls = []
            def fake_command(args, cwd, **kwargs):
                calls.append(args)
                if args[:3] == ["git", "worktree", "add"]:
                    (repo / monthly.STATE / "github-review").mkdir(parents=True)
                if args[:3] == ["git", "branch", "--show-current"]:
                    return monthly.BRANCH
                return ""
            with patch.object(monthly, "command", side_effect=fake_command), patch.object(monthly.subprocess, "run"), patch.object(monthly, "validate_wiki", side_effect=ValueError("broken wiki")):
                with self.assertRaisesRegex(ValueError, "broken wiki"):
                    monthly.sync_github(repo, run, monthly.build_curated(run), sys.executable)
            self.assertFalse(any(args[:2] in (["git", "commit"], ["git", "push"]) for args in calls))


if __name__ == "__main__":
    unittest.main()
