#!/usr/bin/env python3
"""Discover and review post-2023 Malaysian methane values before TIDBRepo upload.

The workflow is deliberately append-only until the final ``upload`` command. Discovery,
PDF retrieval, extraction, and review never write to TIDBRepo or the manuscript database.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sqlite3
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from doi_identifiers import normalize_doi, validated_doi


ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "knowledge_base"
DEFAULT_CONFIG = KB / "config" / "tidbrepo_literature_update.json"
DEFAULT_RUNS = KB / "literature_updates" / "runs"
DEFAULT_DB = KB / "database" / "methane.sqlite"
DEFAULT_SNAPSHOT = KB / "snapshots" / "tidbrepo" / "methane_emission_factor_2026-09-20_afolu_batch_added.json"

REVIEW_FIELDS = [
    "proposal_id", "decision", "reviewer_notes", "doi", "title", "publication_year",
    "screening_score", "raw_value_text", "raw_value", "unit_original", "statistic",
    "evidence_quote", "page", "source_url", "open_access_pdf_url", "pdf_sha256",
    "countries", "sectors", "category", "condition", "tier", "min", "max",
    "median", "mean", "stdev", "scaling_factor", "unit", "url", "doi_1",
]

CANDIDATE_REVIEW_FIELDS = [
    "candidate_id", "paper_decision", "reviewer_notes", "doi", "title",
    "publication_year", "screening_score", "screening_flags", "source_url",
    "open_access_pdf_url", "source_retrieval_status", "extraction_error",
    "proposed_value_count",
]

UPLOAD_FIELDS = [
    "countries", "sectors", "category", "condition", "tier", "min", "max",
    "median", "mean", "stdev", "scaling_factor", "unit", "url", "doi_1",
    "doi_2", "doi_3", "doi_4", "doi_5", "doi_6",
]

NUMBER = r"[-+]?(?:\d+(?:[.,]\d+)?|[.,]\d+)(?:\s*[x×]\s*10\s*[-−^]?\s*\d+|[eE][-+]?\d+)?"
UNIT = (
    r"(?:Gg|Mg|kg|g|mg|µg|ug|t|L|mL|Nm\s*[3³]|m\s*[3³]|ppm|ppb|nmol)"
    r"(?:\s*CH\s*(?:4|₄|⁴))?"
    r"(?:\s*(?:/|per)\s*[A-Za-z0-9µ⁻¹²³⁰-⁹\-\s]+)?"
)
VALUE_UNIT_RE = re.compile(
    rf"(?P<value>{NUMBER})(?:\s*±\s*(?P<uncertainty>{NUMBER}))?\s*(?P<unit>{UNIT})(?![A-Za-z])",
    re.I,
)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
RESULT_CUE_RE = re.compile(
    r"\b(?:emission factor|flux|yield|concentration|mean|median|range|ranged|"
    r"measured|observed|estimated|calculated|achieved|emitted|uptake|production)\b",
    re.I,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_id(prefix: str, *parts: object) -> str:
    raw = "\x1f".join(str(part or "") for part in parts).encode("utf-8")
    return f"{prefix}_{hashlib.sha256(raw).hexdigest()[:16]}"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def request_json(url: str, mailto: str | None = None) -> dict:
    agent = "TIDBRepo-Malaysia-Methane-Literature-Update/1.0"
    if mailto:
        agent += f" (mailto:{mailto})"
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": agent})
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.load(response)


def abstract_from_inverted_index(index: dict | None) -> str:
    if not index:
        return ""
    positions = [(position, word) for word, values in index.items() for position in values]
    return " ".join(word for _, word in sorted(positions))


def work_year(work: dict) -> int | None:
    value = work.get("publication_year")
    return int(value) if value else None


def work_doi(work: dict) -> str:
    ids = work.get("ids") or {}
    return normalize_doi(work.get("doi") or ids.get("doi"))


def oa_pdf_url(work: dict) -> str:
    best = work.get("best_oa_location") or {}
    return best.get("pdf_url") or ""


def has_malaysian_affiliation(work: dict) -> bool:
    for authorship in work.get("authorships") or []:
        for institution in authorship.get("institutions") or []:
            if institution.get("country_code") == "MY":
                return True
    return False


def normalized_title_key(value: str | None) -> str:
    return re.sub(r"\W+", " ", (value or "").lower()).strip()


def existing_candidate_identities(
    db_path: Path,
    snapshot_path: Path,
    runs_dir: Path | None = None,
) -> tuple[set[str], set[str], set[str]]:
    values: set[str] = set()
    openalex_ids: set[str] = set()
    title_keys: set[str] = set()
    if db_path.exists():
        with sqlite3.connect(db_path) as conn:
            for (doi,) in conn.execute("SELECT doi FROM documents WHERE doi IS NOT NULL"):
                if normalize_doi(doi):
                    values.add(normalize_doi(doi))
    if snapshot_path.exists():
        for row in load_json(snapshot_path):
            for key in (f"doi_{index}" for index in range(1, 7)):
                if normalize_doi(row.get(key)):
                    values.add(normalize_doi(row[key]))
    if runs_dir and runs_dir.exists():
        for candidate_path in sorted(runs_dir.glob("*/candidates.jsonl")):
            for row in read_jsonl(candidate_path):
                if normalize_doi(row.get("doi")):
                    values.add(normalize_doi(row["doi"]))
                if row.get("openalex_id"):
                    openalex_ids.add(str(row["openalex_id"]).strip())
                if normalized_title_key(row.get("title")):
                    title_keys.add(normalized_title_key(row["title"]))
    return values, openalex_ids, title_keys


def existing_dois(db_path: Path, snapshot_path: Path) -> set[str]:
    """Backward-compatible DOI-only view used by older callers."""
    values, _, _ = existing_candidate_identities(db_path, snapshot_path)
    return values


def screening_score(title: str, abstract: str, config: dict) -> tuple[int, list[str]]:
    text = f"{title} {abstract}".lower()
    flags: list[str] = []
    score = 0
    country_hits = [term for term in config["country_terms"] if term.lower() in text]
    methane_hits = [term for term in config["methane_terms"] if term.lower() in text]
    measurement_hits = [term for term in config["measurement_terms"] if term.lower() in text]
    exclusion_hits = [term for term in config["exclusion_terms"] if term.lower() in title.lower()]
    if country_hits:
        score += 4
        flags.append("malaysia_context")
    if methane_hits:
        score += 3
        flags.append("methane_context")
    if measurement_hits:
        score += min(3, len(measurement_hits))
        flags.append("measurement_language")
    if re.search(r"\d", abstract) and VALUE_UNIT_RE.search(abstract):
        score += 2
        flags.append("numeric_value_in_abstract")
    if exclusion_hits:
        score -= 4
        flags.append("likely_secondary_source")
    return score, flags


def command_discover(args: argparse.Namespace) -> int:
    config = load_json(args.config)
    run_id = args.run_id or datetime.now().strftime("%Y%m%dT%H%M%S")
    run_dir = args.runs_dir / run_id
    raw_dir = run_dir / "raw" / "openalex"
    raw_dir.mkdir(parents=True, exist_ok=True)
    known, seen_openalex_ids, seen_title_keys = existing_candidate_identities(
        args.db, args.snapshot, args.runs_dir
    )
    works: dict[str, dict] = {}
    retrieved_at = utc_now()

    for query_index, query in enumerate(config["queries"], start=1):
        cursor = "*"
        for page in range(1, int(config["openalex_max_pages_per_query"]) + 1):
            print(
                f"OpenAlex query {query_index}/{len(config['queries'])}, page {page}: {query}",
                flush=True,
            )
            params = {
                "search": query,
                "filter": f"from_publication_date:{config['search_from_date']}",
                "per-page": str(config["openalex_per_page"]),
                "cursor": cursor,
            }
            if args.mailto:
                params["mailto"] = args.mailto
            url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
            payload = request_json(url, args.mailto)
            print(f"  received {len(payload.get('results', []))} works", flush=True)
            write_json(raw_dir / f"q{query_index:02d}_p{page:02d}.json", {"request_url": url, "retrieved_at": retrieved_at, "response": payload})
            for work in payload.get("results", []):
                normalized_title = normalized_title_key(work.get("title"))
                key = work_doi(work) or normalized_title or work.get("id") or stable_id("work", work.get("title"))
                works[key] = work
            cursor = (payload.get("meta") or {}).get("next_cursor")
            if not cursor:
                break

    candidates_by_title: dict[str, dict] = {}
    for key, work in works.items():
        title = (work.get("title") or "").strip()
        abstract = abstract_from_inverted_index(work.get("abstract_inverted_index"))
        score, flags = screening_score(title, abstract, config)
        if has_malaysian_affiliation(work):
            score += 2
            flags.append("malaysian_author_affiliation")
        doi = work_doi(work)
        title_key = normalized_title_key(title)
        openalex_id = work.get("id") or ""
        already_seen_candidate = bool(
            (doi and doi in known)
            or (openalex_id and openalex_id in seen_openalex_ids)
            or (title_key and title_key in seen_title_keys)
        )
        candidate = {
            "candidate_id": stable_id("candidate", doi or key, title),
            "doi": doi,
            "title": title,
            "publication_year": work_year(work),
            "abstract": abstract,
            "source_url": (work.get("primary_location") or {}).get("landing_page_url") or work.get("id"),
            "open_access_pdf_url": oa_pdf_url(work),
            "openalex_id": openalex_id,
            "discovered_by": "OpenAlex API",
            "discovered_at": retrieved_at,
            "screening_score": score,
            "screening_flags": flags,
            "already_known_by_doi": bool(doi and doi in known),
            "already_seen_candidate": already_seen_candidate,
            "workflow_status": "pending_screening",
        }
        # Malaysia and methane are both mandatory. The score only ranks candidates
        # within that eligible set; it must never admit a global paper by itself.
        malaysia_signal = "malaysia_context" in flags or "malaysian_author_affiliation" in flags
        mandatory_context = malaysia_signal and "methane_context" in flags
        if mandatory_context and score >= int(config["minimum_screening_score"]):
            if already_seen_candidate and not args.include_known:
                continue
            previous = candidates_by_title.get(title_key)
            quality = (bool(candidate["doi"]), bool(candidate["open_access_pdf_url"]), candidate["screening_score"])
            previous_quality = (
                bool(previous and previous["doi"]),
                bool(previous and previous["open_access_pdf_url"]),
                previous["screening_score"] if previous else -1,
            )
            if previous is None or quality > previous_quality:
                if previous:
                    candidate["alternate_record_ids"] = [previous.get("openalex_id")]
                candidates_by_title[title_key] = candidate
            elif previous:
                previous.setdefault("alternate_record_ids", []).append(candidate.get("openalex_id"))

    # Targeted web-search results can be frozen in configuration when a newly
    # published paper has not reached OpenAlex yet. They pass through the same
    # screening and human-review gates as API discoveries.
    for seed in config.get("seed_candidates", []):
        title = seed["title"].strip()
        abstract = seed.get("abstract", "")
        score, flags = screening_score(title, abstract, config)
        doi = normalize_doi(seed.get("doi"))
        title_key = normalized_title_key(title)
        already_seen_candidate = bool(
            (doi and doi in known) or (title_key and title_key in seen_title_keys)
        )
        candidate = {
            "candidate_id": stable_id("candidate", doi, title),
            "doi": doi,
            "title": title,
            "publication_year": seed.get("publication_year"),
            "abstract": abstract,
            "source_url": seed.get("source_url", ""),
            "open_access_pdf_url": seed.get("open_access_pdf_url", ""),
            "openalex_id": "",
            "discovered_by": "targeted_web_search_seed",
            "discovered_at": retrieved_at,
            "screening_score": score,
            "screening_flags": flags + ["manual_seed_pending_screening"],
            "already_known_by_doi": bool(doi and doi in known),
            "already_seen_candidate": already_seen_candidate,
            "workflow_status": "pending_screening",
        }
        if already_seen_candidate and not args.include_known:
            continue
        if title_key not in candidates_by_title:
            candidates_by_title[title_key] = candidate
    candidates = list(candidates_by_title.values())
    candidates.sort(key=lambda row: (-row["screening_score"], -(row["publication_year"] or 0), row["title"]))
    write_jsonl(run_dir / "candidates.jsonl", candidates)
    write_json(run_dir / "manifest.json", {
        "run_id": run_id,
        "created_at": retrieved_at,
        "config_sha256": sha256_bytes(args.config.read_bytes()),
        "queries": config["queries"],
        "works_deduplicated": len(works),
        "candidates_retained": len(candidates),
        "known_dois_at_run": len(known),
        "seen_openalex_ids_at_run": len(seen_openalex_ids),
        "seen_titles_at_run": len(seen_title_keys),
        "previously_seen_candidates_included": bool(args.include_known),
        "database_write_performed": False,
    })
    print(run_dir)
    print(f"works={len(works)} candidates={len(candidates)} new_by_doi={sum(not c['already_known_by_doi'] for c in candidates)}")
    return 0


def download_pdf(url: str, path: Path) -> tuple[str, int]:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/pdf"})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    if not data.startswith(b"%PDF"):
        raise ValueError("download did not return a PDF")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha256_bytes(data), len(data)


def pdf_pages(path: Path) -> list[str]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("Install knowledge_base/requirements.txt before extraction") from exc
    return [(page.extract_text() or "") for page in PdfReader(path).pages]


def evidence_sentences(text: str) -> Iterable[tuple[str, re.Match]]:
    compact = re.sub(r"\s+", " ", text).strip()
    for sentence in SENTENCE_RE.split(compact):
        if not re.search(r"methane|CH\s*(?:4|₄|⁴)", sentence, re.I):
            continue
        if not RESULT_CUE_RE.search(sentence):
            continue
        for match in VALUE_UNIT_RE.finditer(sentence):
            # A generic mass/volume elsewhere in a methane sentence is often an
            # activity datum, nitrogen rate, or cited comparator. Keep it only
            # when CH4 is explicit in the unit or the methane label is nearby.
            unit = match.group("unit")
            nearby = sentence[max(0, match.start() - 90):match.end() + 40]
            explicit = bool(re.search(r"CH\s*(?:4|₄|⁴)", unit, re.I))
            methane_nearby = bool(re.search(r"methane|CH\s*(?:4|₄|⁴)", nearby, re.I))
            if not (explicit or methane_nearby):
                continue
            yield sentence[:1200], match


def command_extract(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    candidates = read_jsonl(run_dir / "candidates.jsonl")
    approved_candidate_ids: set[str] | None = None
    if args.screening_decisions:
        decision_payload = load_json(args.screening_decisions)
        approved_candidate_ids = {
            row["candidate_id"]
            for row in decision_payload.get("decisions", [])
            if row.get("decision") == "retrieve_extract"
        }
    pdf_dir = run_dir / "sources"
    proposals: list[dict] = []
    seen_proposals: set[tuple[str, str, str]] = set()
    errors: list[dict] = []
    for candidate in candidates:
        if approved_candidate_ids is not None and candidate["candidate_id"] not in approved_candidate_ids:
            continue
        if approved_candidate_ids is None and candidate.get("screening_score", 0) < args.minimum_score:
            errors.append({"candidate_id": candidate["candidate_id"], "error": f"below_automatic_extraction_score_{args.minimum_score}"})
            continue
        if candidate.get("already_known_by_doi") and not args.include_known:
            continue
        url = candidate.get("open_access_pdf_url") or ""
        if not url:
            errors.append({"candidate_id": candidate["candidate_id"], "error": "no_open_access_pdf_url"})
            continue
        pdf_path = pdf_dir / f"{candidate['candidate_id']}.pdf"
        try:
            if pdf_path.exists():
                pdf_hash = sha256_bytes(pdf_path.read_bytes())
            else:
                pdf_hash, _ = download_pdf(url, pdf_path)
            pages = pdf_pages(pdf_path)
            for page_number, text in enumerate(pages, start=1):
                for quote, match in evidence_sentences(text):
                    raw = match.group(0).strip()
                    dedupe_key = (candidate["candidate_id"], raw.lower(), match.group("unit").lower())
                    if dedupe_key in seen_proposals:
                        continue
                    seen_proposals.add(dedupe_key)
                    proposal_id = stable_id("proposal", candidate["candidate_id"], page_number, raw, quote)
                    proposals.append({
                        "proposal_id": proposal_id,
                        "candidate_id": candidate["candidate_id"],
                        "doi": candidate.get("doi", ""),
                        "title": candidate["title"],
                        "publication_year": candidate.get("publication_year"),
                        "screening_score": candidate["screening_score"],
                        "raw_value_text": raw,
                        "raw_value": match.group("value").replace(",", "."),
                        "uncertainty_text": match.group("uncertainty") or "",
                        "unit_original": match.group("unit").strip(),
                        "statistic": "unspecified_pending_review",
                        "evidence_quote": quote,
                        "page": page_number,
                        "source_url": candidate.get("source_url", ""),
                        "open_access_pdf_url": url,
                        "pdf_sha256": pdf_hash,
                        "extraction_rule": "methane_sentence_value_unit_v1",
                        "verification_status": "proposed_human_review",
                        "provenance_chain": [
                            {"stage": "discovery", "provider": "OpenAlex", "record_id": candidate.get("openalex_id"), "retrieved_at": candidate.get("discovered_at")},
                            {"stage": "source", "url": url, "sha256": pdf_hash},
                            {"stage": "evidence", "page": page_number, "quote": quote},
                            {"stage": "extraction", "rule": "methane_sentence_value_unit_v1", "raw_value_text": raw},
                        ],
                    })
        except Exception as exc:
            errors.append({"candidate_id": candidate["candidate_id"], "url": url, "error": f"{type(exc).__name__}: {exc}"})
    write_jsonl(run_dir / "proposals.jsonl", proposals)
    write_json(run_dir / "extraction_errors.json", errors)
    print(f"proposals={len(proposals)} errors={len(errors)}")
    return 0


def candidate_retrieval_status(proposal_count: int, error: str) -> str:
    """Distinguish an unattempted score gate from a failed source request."""
    if proposal_count:
        return "source_retrieved_values_proposed"
    if error.startswith("below_automatic_extraction_score_"):
        return "not_attempted_pending_screening"
    if error == "no_open_access_pdf_url":
        return "manual_full_text_needed"
    if error:
        return "automatic_retrieval_failed"
    return "no_value_proposed"


def command_review(args: argparse.Namespace) -> int:
    run_dir = args.run_dir
    proposals = read_jsonl(run_dir / "proposals.jsonl")
    candidates = read_jsonl(run_dir / "candidates.jsonl")
    extraction_errors = load_json(run_dir / "extraction_errors.json") if (run_dir / "extraction_errors.json").exists() else []
    error_by_candidate = {row["candidate_id"]: row.get("error", "") for row in extraction_errors}
    proposal_counts: dict[str, int] = {}
    for proposal in proposals:
        proposal_counts[proposal["candidate_id"]] = proposal_counts.get(proposal["candidate_id"], 0) + 1
    retrieval_statuses = {
        candidate["candidate_id"]: candidate_retrieval_status(
            proposal_counts.get(candidate["candidate_id"], 0),
            error_by_candidate.get(candidate["candidate_id"], ""),
        )
        for candidate in candidates
    }

    candidate_csv = run_dir / "candidate_review.csv"
    with candidate_csv.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=CANDIDATE_REVIEW_FIELDS)
        writer.writeheader()
        for candidate in candidates:
            count = proposal_counts.get(candidate["candidate_id"], 0)
            error = error_by_candidate.get(candidate["candidate_id"], "")
            retrieval = retrieval_statuses[candidate["candidate_id"]]
            writer.writerow({
                "candidate_id": candidate["candidate_id"],
                "paper_decision": "pending",
                "reviewer_notes": "",
                "doi": candidate.get("doi", ""),
                "title": candidate.get("title", ""),
                "publication_year": candidate.get("publication_year", ""),
                "screening_score": candidate.get("screening_score", ""),
                "screening_flags": ";".join(candidate.get("screening_flags", [])),
                "source_url": candidate.get("source_url", ""),
                "open_access_pdf_url": candidate.get("open_access_pdf_url", ""),
                "source_retrieval_status": retrieval,
                "extraction_error": error,
                "proposed_value_count": count,
            })
    csv_path = run_dir / "review.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_FIELDS)
        writer.writeheader()
        for proposal in proposals:
            row = {key: proposal.get(key, "") for key in REVIEW_FIELDS}
            row.update({
                "decision": "pending",
                "countries": "Malaysia",
                "url": proposal.get("source_url", ""),
                "doi_1": proposal.get("doi", ""),
            })
            writer.writerow(row)
    md_path = run_dir / "REVIEW.md"
    lines = [
        "# Malaysian methane literature-update review",
        "",
        "> Nothing in this package has been uploaded to TIDBRepo.",
        "",
        "For each row in `review.csv`, verify the PDF page and evidence quote, then set `decision` to `approve`, `reject`, or `needs_changes`. Approved rows must have sector, category, condition, tier, statistic field, target unit, URL, and DOI completed.",
        "",
        "## Provenance chain",
        "",
        "OpenAlex discovery record → open-access source URL → SHA-256-frozen PDF → page-numbered evidence quote → exact printed value/unit → reviewer decision → upload payload.",
        "",
        f"Candidate papers awaiting screening: **{len(candidates)}**",
        f"Proposals awaiting review: **{len(proposals)}**",
        f"Papers not retrieved pending score-gate screening: **{sum(s == 'not_attempted_pending_screening' for s in retrieval_statuses.values())}**",
        f"Papers requiring manual full-text retrieval or a retrieval retry: **{sum(s in ('manual_full_text_needed', 'automatic_retrieval_failed') for s in retrieval_statuses.values())}**",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(candidate_csv)
    print(csv_path)
    print(md_path)
    return 0


def numeric_present(row: dict) -> bool:
    return any(str(row.get(key, "")).strip() for key in ("min", "max", "median", "mean"))


def command_prepare_upload(args: argparse.Namespace) -> int:
    with args.review_csv.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    approved = [row for row in rows if row.get("decision", "").strip().lower() == "approve"]
    errors: list[str] = []
    payload: list[dict] = []
    provenance: list[dict] = []
    for row in approved:
        missing = [key for key in ("countries", "sectors", "category", "condition", "tier", "unit", "url", "doi_1") if not row.get(key, "").strip()]
        if row.get("countries", "").strip().lower() != "malaysia":
            missing.append("countries_must_equal_Malaysia")
        if not numeric_present(row):
            missing.append("one_of_min_max_median_mean")
        if missing:
            errors.append(f"{row.get('proposal_id')}: missing/invalid {', '.join(missing)}")
            continue
        prepared = {key: (row.get(key, "").strip() or None) for key in UPLOAD_FIELDS}
        try:
            for key in (f"doi_{i}" for i in range(1, 7)):
                if prepared.get(key):
                    prepared[key] = validated_doi(prepared[key])
        except ValueError:
            errors.append(f"{row.get('proposal_id')}: invalid DOI format")
            continue
        payload.append(prepared)
        provenance.append({
            "proposal_id": row["proposal_id"], "doi": prepared["doi_1"], "reported_doi": row["doi_1"], "source_url": row["url"],
            "pdf_sha256": row["pdf_sha256"], "page": row["page"],
            "evidence_quote": row["evidence_quote"], "raw_value_text": row["raw_value_text"],
            "reviewer_notes": row["reviewer_notes"], "approved_at": utc_now(),
        })
    if errors:
        print("APPROVAL VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    output = args.output or args.review_csv.with_name("approved_upload_payload.json")
    write_json(output, payload)
    write_json(output.with_name(output.stem + "_provenance.json"), provenance)
    print(output)
    print(f"approved_records={len(payload)} database_write_performed=false")
    return 0


def command_upload(args: argparse.Namespace) -> int:
    if not args.execute:
        print("DRY RUN: no upload performed. Pass --execute and the exact confirmation text after human review.")
        print(f"records={len(load_json(args.payload))}")
        return 0
    if args.confirm != "UPLOAD APPROVED RECORDS TO TIDBREPO":
        print("Upload blocked: confirmation text did not match.", file=sys.stderr)
        return 2
    token = os.environ.get(args.token_env)
    if not token:
        print(f"Upload blocked: environment variable {args.token_env} is not set.", file=sys.stderr)
        return 2
    endpoint = args.endpoint.rstrip("/")
    results = []
    for row in load_json(args.payload):
        data = json.dumps(row).encode("utf-8")
        request = urllib.request.Request(
            endpoint, data=data, method="POST",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            results.append({"status": response.status, "body": response.read().decode("utf-8", "replace")[:2000]})
    receipt = args.payload.with_name(args.payload.stem + "_upload_receipt.json")
    write_json(receipt, {"uploaded_at": utc_now(), "endpoint": endpoint, "results": results})
    print(receipt)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    discover = sub.add_parser("discover", help="Search OpenAlex and stage candidates; never writes TIDBRepo")
    discover.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    discover.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS)
    discover.add_argument("--run-id")
    discover.add_argument("--mailto")
    discover.add_argument("--db", type=Path, default=DEFAULT_DB)
    discover.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    discover.add_argument(
        "--include-known",
        action="store_true",
        help="Include candidates already present in TIDBRepo, the knowledge database, or an earlier run",
    )
    discover.set_defaults(func=command_discover)

    extract = sub.add_parser("extract", help="Download OA PDFs and propose page-traceable values")
    extract.add_argument("run_dir", type=Path)
    extract.add_argument("--include-known", action="store_true")
    extract.add_argument("--minimum-score", type=int, default=8)
    extract.add_argument(
        "--screening-decisions",
        type=Path,
        help="Process only candidates marked retrieve_extract in a researcher-reviewed decision JSON file",
    )
    extract.set_defaults(func=command_extract)

    review = sub.add_parser("review", help="Create the human-review CSV and provenance instructions")
    review.add_argument("run_dir", type=Path)
    review.set_defaults(func=command_review)

    prepare = sub.add_parser("prepare-upload", help="Validate approved rows and create a dry upload payload")
    prepare.add_argument("review_csv", type=Path)
    prepare.add_argument("--output", type=Path)
    prepare.set_defaults(func=command_prepare_upload)

    upload = sub.add_parser("upload", help="Upload an approved payload; dry-run unless explicitly confirmed")
    upload.add_argument("payload", type=Path)
    upload.add_argument("--endpoint", required=True)
    upload.add_argument("--token-env", default="TIDBREPO_API_TOKEN")
    upload.add_argument("--execute", action="store_true")
    upload.add_argument("--confirm", default="")
    upload.set_defaults(func=command_upload)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
