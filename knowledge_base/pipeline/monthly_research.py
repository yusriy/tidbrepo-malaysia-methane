#!/usr/bin/env python3
"""Monthly orchestration, unverified wiki publication, and Gmail outbox.

No TIDBRepo writes, scientific promotion, main-branch merges, or timer changes.
Gmail delivery uses the connected app via a separately scheduled outbox consumer.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import tidbrepo_literature_update as literature

ROOT = Path(__file__).resolve().parents[2]
RUNS = Path("knowledge_base/literature_updates/runs")
STATE = Path("knowledge_base/literature_updates/state")
CURATED = Path("knowledge_base/literature_updates/curated")
QUEUE = Path("knowledge_base/wiki/unverified-literature")
BRANCH = "codex/monthly-literature"
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,100}\Z")


def identifier(value: str) -> str:
    if not SAFE_ID.fullmatch(value):
        raise ValueError("Invalid run or candidate identifier")
    return value


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    temp.replace(path)


def load(path: Path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact(value) -> str:
    # Metadata is data, including when rendered as Markdown.
    return re.sub(r"\s+", " ", str(value or "")).replace("[", "&#91;").replace("]", "&#93;").replace("<", "&lt;").replace(">", "&gt;")


def command(args: list[str], cwd: Path, **kwargs) -> str:
    result = subprocess.run(args, cwd=cwd, check=True, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=kwargs.pop("timeout", 120), **kwargs)
    return result.stdout.strip()


def validate_wiki(repo: Path) -> dict:
    """Resolve Obsidian root, page-relative, and unique short-name links."""
    wiki = repo / "knowledge_base/wiki"
    pages = sorted(wiki.rglob("*.md"))
    names: dict[str, list[Path]] = {}
    for page in pages:
        names.setdefault(page.stem, []).append(page)
    errors = []
    for page in pages:
        for target in re.findall(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", page.read_text()):
            target = target.split("#", 1)[0]
            if not target:
                continue
            target = target.removesuffix(".md") + ".md"
            if not ((wiki / target).is_file() or (page.parent / target).is_file()
                    or ("/" not in target and len(names.get(Path(target).stem, [])) == 1)):
                errors.append(f"{page.relative_to(wiki)} -> {target}")
    for path in (repo / CURATED).glob("*.json"):
        record = load(path)
        if record.get("verification_status") != "unverified":
            errors.append(f"{path.name}: generated literature must be unverified")
        for proposal in record.get("proposals", []):
            required = ("proposal_id", "candidate_id", "doi", "source_url", "pdf_sha256",
                        "page", "evidence_quote", "raw_value_text", "unit_original")
            if any(not proposal.get(key) for key in required):
                errors.append(f"{path.name}: incomplete proposal evidence")
            if proposal.get("verification_status") != "proposed_human_review":
                errors.append(f"{path.name}: measurement promoted without scientific review")
    if errors:
        raise ValueError("Wiki validation failed: " + "; ".join(errors))
    return {"markdown_pages": len(pages), "broken_wikilinks": 0, "curated_provenance": "passed"}


def build_curated(run: Path) -> dict:
    manifest = load(run / "manifest.json")
    if not manifest or not (run / "candidates.jsonl").exists():
        raise ValueError("A completed discovery manifest and candidate list are required")
    candidates = literature.read_jsonl(run / "candidates.jsonl")
    proposals = literature.read_jsonl(run / "proposals.jsonl")
    candidate_fields = ("candidate_id", "doi", "title", "publication_year", "source_url",
                        "open_access_pdf_url", "openalex_id", "discovered_at", "discovered_by",
                        "screening_score", "screening_flags")
    proposal_fields = ("proposal_id", "candidate_id", "doi", "source_url", "open_access_pdf_url",
                       "pdf_sha256", "page", "evidence_quote", "raw_value_text", "raw_value",
                       "unit_original", "uncertainty_text", "statistic", "extraction_rule", "provenance_chain")
    return {
        "run_id": identifier(run.name), "verification_status": "unverified",
        "manifest": manifest,
        "input_sha256": {p.name: sha(p) for p in (run / "manifest.json", run / "candidates.jsonl", run / "proposals.jsonl") if p.exists()},
        "candidates": [{**{k: c.get(k) for k in candidate_fields}, "verification_status": "unverified"} for c in candidates],
        "proposals": [{**{k: p.get(k) for k in proposal_fields}, "verification_status": "proposed_human_review"} for p in proposals],
    }


def queue_index(repo: Path) -> str:
    """Keep owner decisions separate from immutable discovery snapshots."""
    reviews = {}
    for path in sorted((repo / "knowledge_base/literature_updates/reviews").glob("*.json")):
        review = load(path)
        reviews[review["candidate_id"]] = review
    lines = ["# Unverified literature queue", "",
             "> Extracted values remain unverified. Run pages are archived discovery snapshots; recorded owner decisions take precedence.", ""]
    for page in sorted((repo / QUEUE).glob("*.md")):
        if page.name == "index.md":
            continue
        candidates = load(repo / CURATED / (page.stem + ".json"), {}).get("candidates", [])
        closed = [reviews[c["candidate_id"]] for c in candidates
                  if reviews.get(c["candidate_id"], {}).get("decision") in ("exclude", "context_only")]
        pending = len(candidates) - len(closed)
        lines.append(f"- [[unverified-literature/{page.stem}|{page.stem}]] — {pending} pending; {len(closed)} completed paper reviews")
        for review in closed:
            lines.append(f"  - [[{review['wiki_review_page']}|{review['decision']}]] — " + compact(review["title"]))
    return "\n".join(lines).rstrip() + "\n"


def publish_queue(repo: Path, record: dict) -> list[str]:
    run_id = identifier(record["run_id"])
    path = repo / CURATED / f"{run_id}.json"
    if path.exists() and load(path) != record:
        raise ValueError("Curated run already exists with different evidence; use a new attempt ID")
    save(path, record)
    lines = ["# Unverified literature: " + run_id, "",
             "> Machine-discovered candidates and proposed measurements. Scientific review is required.", "",
             "Nothing on this page is a verified inventory value. Promotion to the main scientific wiki is manual after review.", "",
             f"Curated provenance: `knowledge_base/literature_updates/curated/{run_id}.json`", "",
             f"Local review package: `knowledge_base/literature_updates/runs/{run_id}/`", ""]
    for candidate in record["candidates"]:
        lines += ["## " + compact(candidate["title"]), "",
                  "- Status: **unverified; pending scientific review**",
                  "- Candidate ID: " + compact(candidate["candidate_id"]),
                  "- DOI: " + compact(candidate["doi"]),
                  "- Source location: " + compact(candidate["source_url"]),
                  "- OA location: " + compact(candidate["open_access_pdf_url"]),
                  "- Discovery: " + compact(candidate["discovered_by"]) + "; " + compact(candidate["discovered_at"]), ""]
        for proposal in record["proposals"]:
            if proposal["candidate_id"] == candidate["candidate_id"]:
                lines += ["### Proposed measurement " + compact(proposal["proposal_id"]), "",
                          "- Status: **proposed; not verified**",
                          "- Reported value: " + compact(proposal["raw_value_text"]),
                          "- Original unit: " + compact(proposal["unit_original"]),
                          "- PDF page: " + compact(proposal["page"]),
                          "- PDF SHA-256: " + compact(proposal["pdf_sha256"]),
                          "- Evidence quote (unverified): " + compact(proposal["evidence_quote"]), ""]
    queue = repo / QUEUE
    queue.mkdir(parents=True, exist_ok=True)
    page = queue / f"{run_id}.md"
    content = "\n".join(line.rstrip() for line in lines).rstrip() + "\n"
    if page.exists() and page.read_text() != content:
        raise ValueError("Queue page has edits; preserve reviewer history instead of regenerating")
    page.write_text(content)
    index = queue / "index.md"
    index.write_text(queue_index(repo))
    return [str(CURATED / f"{run_id}.json"), str(QUEUE / f"{run_id}.md"), str(QUEUE / "index.md")]


def sync_github(repo: Path, run: Path, record: dict, python: str) -> dict:
    """Commit only generated queue outputs in a dedicated development worktree."""
    checkout = repo / STATE / "github-review"
    checkout.parent.mkdir(parents=True, exist_ok=True)
    if not checkout.exists():
        exists = subprocess.run(["git", "show-ref", "--verify", "--quiet", "refs/heads/" + BRANCH], cwd=repo).returncode == 0
        if exists:
            command(["git", "worktree", "add", str(checkout), BRANCH], repo)
        else:
            command(["git", "worktree", "add", "-b", BRANCH, str(checkout), "HEAD"], repo)
    if command(["git", "branch", "--show-current"], checkout) != BRANCH:
        raise ValueError("Git publication checkout must use the designated development branch")
    if command(["git", "status", "--porcelain"], checkout):
        raise ValueError("Publication checkout has local edits; preserve and review them before retrying")
    files = publish_queue(checkout, record)
    validation = validate_wiki(checkout)
    save(run / "wiki_validation.json", validation)
    try:
        output = command([python, "-m", "unittest", "discover", "-s", "knowledge_base/tests", "-v"], repo, timeout=180,
                         env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        (run / "publication_tests.log").write_text(output + "\n")
    except subprocess.CalledProcessError as exc:
        (run / "publication_tests.log").write_text(exc.stdout or "Tests failed")
        raise
    command(["git", "add", "--", *files], checkout)
    staged = command(["git", "diff", "--cached", "--name-only"], checkout).splitlines()
    if set(staged) - set(files):
        raise ValueError("Unexpected files staged; refusing publication")
    command(["git", "diff", "--cached", "--check"], checkout)
    if staged:
        command(["git", "commit", "-m", "Queue unverified Malaysian methane literature " + run.name], checkout)
    # Explicit destination: neither current live branch nor main can be pushed here.
    command(["git", "push", "origin", "HEAD:refs/heads/" + BRANCH], checkout)
    remote = command(["git", "remote", "get-url", "origin"], checkout)
    match = re.fullmatch(r"https://github.com/([\w.-]+/[\w.-]+?)(?:\.git)?", remote)
    review_url = ("https://github.com/" + match[1] + "/tree/" + urllib.parse.quote(BRANCH, safe="") +
                  "/knowledge_base/wiki/unverified-literature/index.md") if match else None
    return {"status": "pushed", "branch": BRANCH, "review_url": review_url,
            "commit": command(["git", "rev-parse", "HEAD"], checkout),
            "wiki_queue": str(checkout / QUEUE / (run.name + ".md"))}


def summarize(run: Path, state: dict) -> dict:
    manifest = load(run / "manifest.json", {})
    candidates = literature.read_jsonl(run / "candidates.jsonl")
    proposals = literature.read_jsonl(run / "proposals.jsonl")
    errors = {e["candidate_id"]: e.get("error", "") for e in load(run / "extraction_errors.json", [])}
    return {
        **state, "run_id": run.name,
        "publications_screened": manifest.get("works_deduplicated"),
        "screening_definition": "Unique OpenAlex works evaluated by deterministic title/abstract screening; manual seeds are separate",
        "manual_seed_candidates": sum(c.get("discovered_by") == "targeted_web_search_seed" for c in candidates) if manifest else None,
        "new_candidate_papers": len(candidates) if manifest else None,
        "methane_measurements_proposed": len(proposals) if (run / "proposals.jsonl").exists() else None,
        "papers_requiring_manual_review": [{"candidate_id": c["candidate_id"], "title": c.get("title"),
            "doi": c.get("doi"), "reason": errors.get(c["candidate_id"]) or "pending_scientific_review"} for c in candidates],
        "review_files": [str(run / name) for name in ("candidate_review.csv", "review.csv", "REVIEW.md") if (run / name).exists()],
        "run_directory": str(run), "tidbrepo_upload_performed": False,
    }


def render_summary(summary: dict) -> str:
    def count(key):
        value = summary.get(key)
        return "unavailable (stage incomplete)" if value is None else str(value)
    manual = summary.get("papers_requiring_manual_review", [])
    lines = [f"Malaysian methane literature run {summary['run_id']}: {summary['status'].upper()}",
             "Publications screened: " + count("publications_screened") + " (unique OpenAlex works)",
             "New candidate papers: " + count("new_candidate_papers"),
             "Methane measurements proposed (unverified): " + count("methane_measurements_proposed"),
             "Papers requiring manual review: " + (str(len(manual)) if summary.get("new_candidate_papers") is not None else "unavailable")]
    for paper in manual[:5]:
        lines.append("- " + compact(paper["title"]) + " — " + compact(paper["reason"]))
    if len(manual) > 5:
        lines.append(f"- {len(manual) - 5} additional papers listed in the review package")
    lines += ["Review files: " + (", ".join(summary.get("review_files", [])) or "not generated; see " + summary["run_directory"]),
              "GitHub synchronization: " + summary.get("github", {}).get("status", "not_attempted")]
    if summary.get("github", {}).get("wiki_queue"):
        lines.append("Wiki queue: " + summary["github"]["wiki_queue"])
    if summary.get("github", {}).get("review_url"):
        lines.append("GitHub review: " + summary["github"]["review_url"])
    if summary.get("failed_stage"):
        lines.append("Failed stage: " + summary["failed_stage"])
    return "\n".join(lines) + "\n"


def write_notification(repo: Path, run: Path, state: dict) -> dict:
    summary = summarize(run, state)
    save(run / "run_summary.json", summary)
    (run / "READY_FOR_REVIEW.txt").write_text(render_summary(summary))
    outbox = repo / STATE / "notifications" / (run.name + ".json")
    previous = load(outbox, {})
    save(outbox, {"run_id": run.name, "delivery": previous.get("delivery", "pending"),
                  "gmail_message_id": previous.get("gmail_message_id"), "summary": summary,
                  "subject": f"Malaysian methane literature: {summary['status']} ({run.name})",
                  "body": render_summary(summary)})
    return summary


def run_monthly(repo: Path, python: str, run_id: str, push: bool) -> int:
    run = repo / RUNS / identifier(run_id)
    if run.exists():
        raise ValueError("Run already exists; original evidence must not be overwritten")
    run.mkdir(parents=True)
    started = literature.utc_now()
    state = {"status": "running", "started_at": started, "stages": {}, "github": {"status": "not_attempted"}}
    save(run / "run_status.json", state)
    (repo / STATE).mkdir(parents=True, exist_ok=True)
    (repo / STATE / "latest_run_path.txt").write_text(str(run) + "\n")
    pipeline = repo / "knowledge_base/pipeline/tidbrepo_literature_update.py"
    discovery_ok = False
    stage = "discovery"
    try:
        steps = [("discovery", ["discover", "--runs-dir", str(repo / RUNS), "--run-id", run.name]),
                 ("extraction", ["extract", str(run)]), ("review", ["review", str(run)])]
        if os.environ.get("TIDBREPO_CONTACT_EMAIL"):
            steps[0][1].extend(["--mailto", os.environ["TIDBREPO_CONTACT_EMAIL"]])
        for stage, args in steps:
            state["active_stage"] = stage
            save(run / "run_status.json", state)
            with (run / (stage + ".log")).open("w") as output:
                subprocess.run([python, str(pipeline), *args], cwd=repo, check=True,
                               stdout=output, stderr=subprocess.STDOUT, timeout=1800)
            state["stages"][stage] = "succeeded"
            discovery_ok |= stage == "discovery"
        state["status"] = "succeeded"
    except (Exception, KeyboardInterrupt) as exc:
        state.update(status="failed", failed_stage=stage, failure_type=type(exc).__name__)
        state["stages"][stage] = "failed"
    finally:
        if discovery_ok:
            try:
                record = build_curated(run)
                save(run / "curated_metadata.json", record)
                if push:
                    state["github"] = sync_github(repo, run, record, python)
                else:
                    state["github"] = {"status": "disabled", "reason": "Enable TIDBREPO_GIT_SYNC after deployment review"}
            except Exception as exc:
                state.update(status="failed", failed_stage=state.get("failed_stage", "wiki_github"))
                state["github"] = {"status": "failed", "failure_type": type(exc).__name__}
                (run / "publication_error.log").write_text(str(exc) + "\n")
        state["finished_at"] = literature.utc_now()
        save(run / "run_status.json", state)
        summary = write_notification(repo, run, state)
        print(render_summary(summary))
    return 0 if state["status"] == "succeeded" else 1


def pending_notifications(repo: Path) -> list[dict]:
    # Recover a hard-killed run, including termination by systemd's 45-minute timeout.
    for path in sorted((repo / RUNS).glob("*/run_status.json")):
        state = load(path)
        if state["status"] == "running" and datetime.fromisoformat(state["started_at"]) < datetime.now(timezone.utc) - timedelta(minutes=60):
            state.update(status="failed", failed_stage=state.get("active_stage", "interrupted"),
                         failure_type="InterruptedRun", finished_at=literature.utc_now())
            save(path, state)
            write_notification(repo, path.parent, state)
    return [load(p) for p in sorted((repo / STATE / "notifications").glob("*.json")) if load(p)["delivery"] == "pending"]


def delivery_update(repo: Path, run_id: str, action: str, message_id: str | None = None) -> dict:
    path = repo / STATE / "notifications" / (identifier(run_id) + ".json")
    with path.open("r+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        data = json.load(handle)
        if action == "claim":
            if data["delivery"] != "pending":
                raise ValueError("Notification is already claimed or sent; do not send it twice")
            data["delivery"] = "sending"
        else:
            if data["delivery"] != "sending" or not message_id:
                raise ValueError("A claimed notification and confirmed Gmail message ID are required")
            data.update(delivery="sent", gmail_message_id=message_id, sent_at=literature.utc_now())
        handle.seek(0)
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.truncate()
    return data


def interrupted(_signum, _frame):
    raise KeyboardInterrupt


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="action", required=True)
    run = sub.add_parser("run")
    run.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    run.add_argument("--push", action="store_true", default=os.environ.get("TIDBREPO_GIT_SYNC") == "1")
    sub.add_parser("validate-wiki")
    sub.add_parser("pending-notifications")
    for name in ("claim-notification", "ack-notification"):
        cmd = sub.add_parser(name)
        cmd.add_argument("run_id")
        if name == "ack-notification":
            cmd.add_argument("--gmail-message-id", required=True)
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    if args.action == "run":
        signal.signal(signal.SIGTERM, interrupted)
        return run_monthly(repo, sys.executable, args.run_id, args.push)
    if args.action == "validate-wiki":
        print(json.dumps(validate_wiki(repo)))
    elif args.action == "pending-notifications":
        print(json.dumps(pending_notifications(repo), ensure_ascii=False))
    else:
        result = delivery_update(repo, args.run_id,
                                 "claim" if args.action == "claim-notification" else "ack",
                                 getattr(args, "gmail_message_id", None))
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
