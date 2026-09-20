---
managed_by: "human-guided monthly literature workflow"
verification_status: "value_review_complete_staged"
run_id: "2026-08-30-final"
---

# Monthly candidate screening — 30 August 2026

This is the first paper-level screening package for literature published after the retained 26 August 2023 search. It is separate from the 26-paper local corpus and the 16-paper manuscript baseline.

## Human screening outcome

| Saved decision | Papers | Workflow status |
|---|---:|---|
| Retrieve/extract values | 13 | Advanced to curated value review |
| Exclude | 14 | Closed at paper-screening stage |
| Please select | 32 | Optional lower-priority candidates; not a blocker |

## Curated extraction status

- Twelve approved papers have locally archived, checksummed full texts; several were supplied manually by the researcher after automatic retrieval failed.
- The EGU conference abstract remains context-only. No value approved for TIDBRepo staging depends on its missing full paper.
- For `candidate_7e9e03a4115f4b61`, the article PDF and official supplemental DOCX are archived. Supplemental Table S1 replaces the abstract's approximate methane value with seven date- and land-use-specific means and standard deviations; these remain subject to human review before any TIDBRepo staging.
- For `candidate_d3b4b8d8fc03840a`, the publisher PDF is archived. Table 2 replaces the abstract-only hotspot statement with three exact Pond 4 campaign means, standard deviations, and sample sizes. These are Malaysian POME surface fluxes, not a new `kg CH4 kg-1 BOD` factor; conversion is blocked without contemporaneous BOD loading and a defensible area/throughput allocation. The paper's `0.225 kg CH4 kg-1 COD` value is a cited existing national-inventory comparator, not a new measurement.
- For `candidate_bb4619382aa0662a`, the PeerJ PDF is archived. Nine full-text methane-flux records replace two abstract-only rows and cover Kenyir Reservoir diffusion and ebullition, the Terengganu River, and high/low-flow plus neap/spring-tide conditions in the estuary. Each reported `mmol CH4 m-2 day-1` value has a documented direct conversion to `kg CH4 ha-1 day-1` using a factor of `0.16`; `16/12` is not used because the source already reports methane rather than carbon mass.
- Sixty-six Malaysia-relevant value rows were curated and all human decisions are complete: 55 were approved for wiki and TIDBRepo staging, while 11 were retained as wiki context only. The remote-sensing paper remains paper-level context because no defensible Malaysia-specific quantified plume was identified.
- The curated workbook is `outputs/01a0507e-5e8e-7dc2-be97-52906a1658b5/monthly_value_extraction_review_2026-08-30.xlsx`.

## Safety and provenance status

- No candidate has been added to the 26-paper corpus.
- No candidate or value has been uploaded to TIDBRepo.
- The 76 values from the first automatic extraction are quarantined because the original rule captured PDF line-number noise and method constants.
- Only papers explicitly approved for `Retrieve/extract values` may proceed to full-text extraction.
- The source manifest remains in `knowledge_base/literature_updates/runs/2026-08-30-final/`.
- The completed paper-screening workbook is `outputs/01a0507e-5e8e-7dc2-be97-52906a1658b5/monthly_candidate_screening_2026-08-30.xlsx`.
- The saved decision gate is `knowledge_base/literature_updates/runs/2026-08-30-final/screening_decisions.json`.

## Current gate

The completed decisions have been imported into the provenance-backed wiki staging area described in [[monthly-value-review-2026-08-30|Monthly value review — 30 August 2026]]. The remaining gate is the category/tier/unit crosswalk review. Nothing has been uploaded to TIDBRepo.
