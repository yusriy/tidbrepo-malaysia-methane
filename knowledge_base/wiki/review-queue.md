# Human verification queue

> Nothing in this queue becomes verified merely because it was extracted or linked by an LLM.

## Monthly literature

**Current focus: new papers discovered by the automated routine.** August–October paper screening is complete. Original-corpus R01/R02 assessments below are legacy history, not newly discovered papers or required monthly reviews. R01 follow-up is deferred following the owner’s scope clarification on 29 October 2026.

See [[unverified-literature/index|Unverified monthly literature queue]] for machine-discovered candidates. These entries and extracted measurements remain unverified until scientific review.

October 2026: **0 pending paper reviews**. The owner [[findings/literature-review-hcc-2026-10-28|excluded the Hydrothermal Compost Catalyst paper]] on 28 October 2026. The older verification items below are separate from this completed monthly review.

August 2026: **0 pending paper-screening decisions**. The owner [[findings/august-2026-remaining-screening-review|approved all 32 saved suggestions]] on 28 October 2026: 4 context-only and 28 excluded. The 66 value-review decisions are already complete; six landfill records retain their existing activity-basis/conversion blockers.

September 2026: **0 pending paper-screening decisions; R04/S02 approved for wiki-only use**. The three extracted proposals remain unverified, with source conflicts retained; no database submission is pending. The owner excluded S01 and retained S02 for extraction. See [[findings/september-2026-screening-and-extraction-review|the source-checked S03–S05 review]] for the approved wiki-only disposition, conflicting reported figures and corrected batch range. The current local measurement review file is `knowledge_base/literature_updates/runs/20261028-september-source-review/review.csv`; the original September run remains archived unchanged.

## Queue summary

The original corpus has been [[findings/original-corpus-tidbrepo-reconciliation-2026-10-28|matched against all 180 live TIDBRepo records]]. Eleven of the 18 papers with extracted measurements are already cited. Six extracted values match stored numbers after normalization; other records include combined-source ranges, concentrations, regional totals and extraction errors. The 95 `proposed` measurements below are local scientific-verification flags, **not 95 missing uploads or 95 new approval requests**. Use the focused checks in the reconciliation report before deciding whether anything needs adding.

- Bibliographic title overrides to confirm: 8
- Documents without a detected DOI: 1
- Documents without a separately detected abstract: 3
- Proposed topic assignments: 155
- Proposed claims: 67
- Proposed measurements: 95
- Open editor/reviewer items: 32

## Bibliographic priority

- [[papers/2005-methane-fluxes-from-three-ecosystems-in-tropical-peatland-of-sarawak-malaysia-e285b6|Methane fluxes from three ecosystems in tropical peatland of Sarawak, Malaysia]] — title override
- [[papers/2017-local-emission-factors-estimates-for-methane-emission-from-cattle-enteric-fermen-b782a0|Local emission factors estimates for methane emission from cattle enteric fermentation using IPCC tier-2 methodology]] — title override, DOI missing
- [[papers/2017-methane-emission-from-pineapple-cultivation-on-a-tropical-peatland-at-saratok-ma-c4ef44|Methane Emission from Pineapple Cultivation on a Tropical Peatland at Saratok, Malaysia]] — title override
- [[papers/2019-nitrous-oxide-n2o-and-methane-ch4-in-rivers-and-estuaries-of-northwestern-borneo-54f5b9|Nitrous oxide (N2O) and methane (CH4) in rivers and estuaries of northwestern Borneo]] — title override
- [[papers/2020-greenhouse-gas-emissions-resulting-from-conversion-of-peat-swamp-forest-to-oil-p-2a5067|Greenhouse gas emissions resulting from conversion of peat swamp forest to oil palm plantation]] — abstract boundary missing
- [[papers/2021-greenhouse-gas-emission-intensity-assessment-for-power-plants-in-peninsular-mala-9fd431|Greenhouse Gas Emission Intensity Assessment for Power Plants in Peninsular Malaysia]] — title override
- [[papers/2022-impact-of-interannual-and-multidecadal-trends-on-methane-climate-feedbacks-and-s-1a30d7|Impact of interannual and multidecadal trends on methane-climate feedbacks and sensitivity]] — abstract boundary missing
- [[papers/2022-mapping-trends-of-carbon-dioxide-and-methane-during-movement-control-order-in-in-137b06|Mapping Trends of Carbon Dioxide and Methane During Movement Control Order in Industrial Areas in Peninsular Malaysia Using GOSAT, GOSAT-2, OCO-2, OCO-3, and TROPOMI Satellites Data]] — title override
- [[papers/2023-assessing-machine-learning-tools-for-methane-emission-prediction-from-pome-treat-2f7f43|Assessing machine learning tools for methane emission prediction from POME treatment in Malaysia]] — title override
- [[papers/2023-rekod-jangka-panjang-kepekatan-metana-di-malaysia-long-term-record-of-methane-in-1e7f87|Rekod Jangka Panjang Kepekatan Metana di Malaysia (Long Term Record of Methane in Malaysia)]] — title override
- [[papers/2023-rice-and-paddy-industry-in-malaysia-governance-and-policies-research-trends-tech-909d7d|Rice and paddy industry in Malaysia: governance and policies, research trends, technology adoption and resilience]] — abstract boundary missing

## Verification procedure

1. Open the linked paper and confirm the title, authors, DOI, and section boundaries.
2. For a claim, inspect its chunk and exact PDF page before changing `verification_status`.
3. For a measurement, confirm sign, unit, statistic, conditions, and whether the value belongs to this study rather than a cited study.
4. For reviewer evidence, confirm that each suggested passage actually addresses the comment; remove irrelevant suggestions.
5. Recompile and lint the wiki after database status changes.

## Approved suitability dispositions — R01–R04

The owner approved [[findings/original-corpus-tidbrepo-reconciliation-2026-10-28|R01–R04 suitability decisions]]: R01 and R02 wiki-only with database use on hold; R03 a factor candidate pending full-text verification; R04 wiki-only. These are not new quantitative verification or upload approvals. The later R03 upload is complete. R01/R02 database-assessment checks were on hold at this stage; the owner later accepted R01 staging pending visual Table 2 checking and retained R02 wiki-only, as recorded below. Q01/Q02 existing-entry checks were closed by the owner on 29 October 2026, as recorded below.

## R03 upload follow-up — 29 October 2026

The owner authorized [[papers/2019-carbon-dioxide-and-methane-emissions-from-peat-soil-in-an-undrained-tropical-pea-a6bc32|R03 submission]]. The non-trenched n=9 outlier-excluded Table 3 mean/SD and source conditions have been cross-checked in full text; conversion and duplicate checks passed. One record was uploaded and independently verified as **TIDBRepo row 181** (mean 0.158, SD 0.144 kg CH4 ha^-1 day^-1). The table now contains 181 rows; the original 180 rows are unchanged. R03 has no pending upload action. Earlier candidate-only decisions and the 28 October live-table reconciliation remain historical snapshots. R01/R02/R04 dispositions are unchanged. Q01/Q02 were subsequently closed by the owner, as recorded below.

## Existing-entry checks closed — 29 October 2026

- **Q01 — Melling sago, row 97: closed.** The owner accepted the approximately 0.25% conversion difference as negligible and instructed that it can be ignored. Keep the existing database value unchanged; no correction or further review is required.
- **Q02 — 2014 paddy, rows 109–110: closed.** The owner confirmed this issue was resolved previously. This records the owner's confirmation without inventing an undocumented technical resolution. No new database action or review is required.

Separate decision records preserve the closure and original evidence: `knowledge_base/reconciliations/reviews/2026-10-29-close-Q01.json` and `2026-10-29-close-Q02.json`. These closures do not change scientific verification flags or database values. R03 upload is complete; The owner subsequently staged R01 pending visual Table 2 checking and retained R02 wiki-only; R04 remains wiki-only.

## Guided R01/R02 assessment — 29 October 2026

Source assessment is prepared; the subsequent owner decisions are recorded below: [[papers/2018-micrometeorological-measurement-of-methane-flux-above-a-tropical-peat-swamp-fore-d38a20|R01]] has an author-preferred 9.8–10.8 g CH4-C m^-2 yr^-1 ecosystem-scale processing-estimate range; [[papers/2019-are-secondary-forests-second-rate-comparing-peatland-greenhouse-gas-emissions-ch-20dfb6|R02]] has seasonal soil uptake/emission observations with source-precision, uncertainty and coverage limitations. Recommended next choices are R01 range staging and R02 wiki-only pending exact figure results. The owner subsequently accepted R01 staging pending visual Table 2 checking and R02 wiki-only. No measurements are newly verified or uploaded.

## Legacy R01/R02 dispositions — outside the monthly review queue

- **R01: staged legacy evidence; further review deferred.** One author-preferred ecosystem-scale range candidate (9.8–10.8 g CH4-C m^-2 yr^-1) is preserved with source, conversion and explicit method-range meaning. The visual Table 2 gate remains incomplete, but it is not an active monthly review task. Staging is not upload approval; `ready_for_upload` is false.
- **R02: wiki-only; no pending database action.** Preserve signed seasonal findings and source limitations.

Staged object: `knowledge_base/reconciliations/staging/r01-author-preferred-range-2026-10-29.json`. Decisions: `knowledge_base/reconciliations/reviews/2026-10-29-factor-decision-R01.json` and `2026-10-29-factor-decision-R02.json`. R03 remains uploaded; Q01/Q02 remain closed.
