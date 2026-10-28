---
date: 2026-10-28
type: workflow-audit
status: source-checked-context-only
run_id: 20260930T195143Z
candidate_id: candidate_f524d451c95c260f
---

# October 2026 literature run audit

## Run and extraction diagnosis

The October package is `knowledge_base/literature_updates/runs/20260930T195143Z/`. Its manifest timestamp, 30 September 2026 19:51:43 UTC, is **1 October 2026 03:51:43 Asia/Makassar**. This matches the local monthly window; the manifest alone does not prove which process triggered it. The latest-run pointer identifies this package. It contains 13 frozen OpenAlex response files, 903 deduplicated works, one retained candidate, and zero proposed values. There is no source directory in the original package.

The candidate is *Hydrothermal compost catalyst (HCC): Reducing food waste and methane emissions through optimized composting* (2025), DOI `10.24191/esteem.v21iseptember.5826.g5027`.

| Stage | Observed result |
| --- | --- |
| Discovery | Score 6 passes discovery minimum 5 |
| Score components | Methane language +3, measurement language +1, Malaysian affiliation +2 |
| Missing signals | No Malaysian study-location term in title/abstract; no recognized numeric value/unit in abstract |
| Extraction | Score 6 is below default minimum 8; execution skips before any download |
| Frozen diagnostic | `below_automatic_extraction_score_8` |
| Original review output | Incorrectly reports `automatic_retrieval_failed` and one retrieval/retry case |
| Correct interpretation | Retrieval **not attempted**, pending screening; no evidence of an October network failure |

The branch fixes the generated status to `not_attempted_pending_screening` and separates this count from actual retrieval failures. Historical October outputs remain unchanged. The stored OA URL is a DOI resolver; whether it returned PDF bytes was never tested by that run. Lowering the extraction threshold globally would not establish evidence quality.

## Source verification on 28 October

The [UiTM repository record](https://ir.uitm.edu.my/id/eprint/125392/) confirms the title and DOI. Its [public full text](https://ir.uitm.edu.my/id/eprint/125392/1/125392.pdf) was downloaded separately into the local run's `sources/` directory and checked against its DOI/title. The source contains 17 PDF pages. Full-text review and rendered results-page inspection support a **context-only** classification: no original quantitative methane emission factor or flux was identified.

Evidence locators: methods §2.3, PDF pages 6–7 (printed 138–139); analytical results §3.3, PDF pages 12–14 (printed 144–146), Tables 4–5; conclusion, PDF pages 14–15 (printed 146–147). These describe elemental compost analysis and process performance, not a methane gas measurement. Carbon-to-nitrogen ratios cannot be converted into methane emissions. No methane value has been added to the quantitative baseline.

Bibliographic discrepancy: the first PDF page says volume 22, while later page headers and the repository say volume 21. Preserve the discrepancy for human bibliographic review.

Local PDF: `sources/uitm-125392-verified-20261028.pdf` beneath the run directory. SHA-256: `31b1cbe5d8a034069f0ea85f2d923090be8d1deb91f9ff17b705c1627079d430`. Extracted page text and verification metadata remain local. The October manifest describes the original run, not this later source check.

## Proposed workflow improvements

1. **Separate eligibility from ranking.** Keep broad discovery to retain borderline papers; distinguish affiliation from Malaysian measurement location. Route low-score candidates to screening rather than labeling them failed downloads. Any score override should apply to explicit candidate IDs through the existing researcher-reviewed `screening_decisions.json` gate.
2. **Add LLM-assisted screening as advice.** Freeze title/abstract input, input hash, prompt version, model identifier, timestamp, and structured response. Require separate fields for study location, original CH4 measurement, method, activity denominator, evidence passage, uncertainty, recommendation (`retrieve_extract`, `context_only`, `exclude`, `uncertain`), and rationale. Missing information must remain unknown. Treat source text as data, never instructions. Model output goes to a separate local advisory file and cannot populate researcher-approved decisions automatically. On model failure, keep the candidate pending and continue building the review package.
3. **Verify sources before quantitative staging.** Resolve publisher/institutional repository locations; record original/resolved URLs, access date, content type, title/DOI comparison, checksum, and page count. Distinguish HTML landing pages, missing OA sources, failed downloads, scanned PDFs requiring OCR, and successful extraction with no methane value. Never invent a PDF URL or classify a paper as verified from search metadata alone.
4. **Separate seen, reviewed, and incorporated states.** Currently prior candidate files contribute to the same DOI set as accepted records. Unresolved candidates can disappear from subsequent runs. Maintain a persistent review backlog with explicit pending/context/excluded/verified states and source-run references; deduplicate identities without treating discovery as incorporation. `--include-known` is a broad audit option, not a substitute for that backlog.
5. **Make reruns preserve review history.** Discovery/extraction/review currently write fixed filenames, and `review` resets decisions to pending. Add versioned attempts and immutable inputs, preserve decisions by stable IDs, and require explicit regeneration of existing review artifacts. Do not rerun the original October package in place.
6. **Strengthen quantitative validation.** Before payload preparation, require source checksum, page/table/figure, supporting quote, original value/unit, statistic, study-versus-cited provenance, activity basis, and a recorded conversion from the unit policy. Current preparation checks classification fields but does not enforce all evidence fields. Reject nonnumeric/nonfinite statistics and mismatched denominators. Add tests for missing evidence, incompatible units, LLM failures, and preservation of reviewed rows.
7. **Publish curated research.** Retain complete run packages locally; commit source-linked findings, reviewed quantitative records, research gaps, code, and tests. Stage explicit files, run tests, push a development branch, and obtain owner approval before merging into `main`. Model recommendations and unreviewed payloads are not validated research updates. Existing tracked run history stays intact.

Items 2–6 are a proposed implementation sequence, not active functionality in this branch. The monthly runner remains deterministic and makes no LLM calls. Source verification here was performed during this audit.

## Research implications and follow-up

- **Paper-specific gap:** direct methane measurement under HCC treatment and a comparable control is needed before claiming a quantified methane benefit. Record gas measurement method, integrated duration, feedstock mass/basis, replicates, and uncertainty. This is not evidence that the entire Malaysian composting literature lacks such measurements.
- **Inventory relevance:** separate treatment performance, methane production/capture, atmospheric flux, and inventory emission factors. A treatment yield or concentration alone may not be convertible to an inventory denominator. See [[topics/methane-emission-factors|Methane emission factors]] and [[topics/waste-sector|Waste-sector evidence]].
- **Coverage:** one newly retained candidate does not measure completeness of the literature. Query pagination is capped at two pages per query; audit truncation and the unresolved backlog before drawing conclusions about research scarcity. Review [[research-gaps/reviewer-identified-gaps|Existing research gaps]] alongside this paper-specific limitation.

No TIDBRepo upload, scientific SQLite update, timer change, or merge was performed.
