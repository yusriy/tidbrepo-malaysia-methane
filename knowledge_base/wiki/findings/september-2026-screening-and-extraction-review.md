---
date: 2026-10-28
status: extracted-pending-scientific-review
source_run_id: 20260920T164325
extraction_attempt: 20261028-september-source-review
---

# September 2026: owner screening and source extraction

The owner instructed: “S01 exclude, S02 retain, SO3-S05, extract.” The numbering identifies S03–S05; “extract” authorizes source extraction, not approval of the resulting measurements.

| Paper ID | Paper | Owner decision |
|---|---|---|
| S01 | Biogas Recovery from Palm Oil Mill Effluent in Malaysia: A Review of Technology Transition, Deployment Readiness, and Sustainability Challenges; DOI `10.3390/biomass6050077` | Exclude |
| S02 | Production of Methane and Hydrogen from Mild-Strength Industrial Wastewater; DOI `10.14233/ajchem.2024.30618` | Retain for quantitative assessment; retrieve/extract |

**Paper screening is complete: 0 pending. The owner subsequently selected wiki-only use for R04/S02 on 28 October 2026. The three proposals remain unverified; source conflicts remain unresolved, but there is no outstanding choice of database versus wiki use.** Each paper decision is recorded separately in `knowledge_base/literature_updates/reviews/2026-10-28-september-S01.json` and `2026-10-28-september-S02.json`.

## Archived source and study context

S02: Siddique et al. (2024), *Asian Journal of Chemistry*, 36(4), 935–942. DOI/source: https://doi.org/10.14233/ajchem.2024.30618. Publisher PDF location: https://asianpubs.org/index.php/ajchem/article/download/36_4_23/29576.

The locally archived PDF has eight pages and SHA-256 `03af1e9be60fe3ab2390bc7f851ea6dba74fc093bccae6a80d17c0823210c99d`. Its Experimental section, PDF page 2 (printed 936), identifies industrial wastewater from Terengganu, Malaysia. The same section describes GC-TCD gas-composition analysis and a wet gas meter. These are reactor methane-production/recovery measurements, not independently established atmospheric emission factors. The industry is not assumed to be palm oil merely because the other candidate is a POME review.

PDF text and rendered pages 3–6 were inspected, including Tables 1, 2, 4 and 5. Missing fontTools warnings in the first text-extraction attempt were addressed through layout text extraction and visual inspection rather than silently trusting the text stream.

## S03: methane production rate — source disagreement retained

For continuous Run 2, hydrogen-stage HRT 8 h and methane-stage HRT 24 h:

| Source location | Exact reported entry | Unit |
|---|---|---|
| Abstract; PDF p. 1 (935) | 71 ± 30 | mL/L-d |
| Table 2, Run 2 CH4 row; PDF p. 4 (938) | 71.0 ± 31.0 | mL/Ld |
| Results prose; PDF p. 5 (939) | 71 ± 30 | mL/L-d |
| Table 5, Run 2 CH4 row; PDF p. 6 (940) | 72.0 ± 31.0 | mL/L-d |

The original abstract value is retained alongside all variants. No preferred value is chosen automatically. The meaning of the ± term is not assumed to be standard deviation.

## S04: methane yield — source disagreement retained

For the same continuous operating condition:

| Source location | Exact reported entry | Unit |
|---|---|---|
| Abstract; PDF p. 1 (935) | 57 ± 10 | mL/g COD |
| Table 2, Run 2 CH4 row; PDF p. 4 (938) | 57.0 ± 12.0 | mL/g COD |
| Results prose; PDF p. 5 (939) | 57 ± 11 | mL/g COD |
| Table 4, this-study suspended-cell CH4 row; PDF p. 6 (940) | 58.0 ± 12.0 | mL/gCOD |
| Table 5, Run 2 CH4 row; PDF p. 6 (940) | 58.0 ± 12.0 | mL/g COD |

Table 4 lists 25°C, while the methods discuss 35°C operation; that discrepancy is also retained for review. An author clarification or an explicit reviewer choice with rationale is needed to resolve which reported representation to use.

## S05: corrected batch methane-volume extraction

The initial regex proposal captured only `66 mL`. The source sentence on PDF page 3 (937) reports a **56–66 mL range after 45 days**, and Table 1 gives these individual conditions:

| Nitrogen source | Inoculum | CH4 volume, mL |
|---|---|---:|
| NH4Cl | Cow waste | 66 |
| NH4Cl | Sewage sludge 1 | 60 |
| NH4Cl | Sewage sludge 2 | 56 |
| Urea | Cow waste | 57 |
| Urea | Sewage sludge 1 | 59 |
| Urea | Sewage sludge 2 | 56 |

The new S05 proposal records the range and its six component observations, with the mesophilic batch context. It does not present 66 mL as a mean. The original 66 mL automatic proposal remains archived as extraction history.

## Review and unit-conversion boundary

All three records remain **proposed_human_review**. S03 and S04 require resolution of inconsistent source values/uncertainties. S05 requires review as a condition-specific batch result or range, rather than a standalone inventory factor.

No standardized `kg CH4 kg-1 BOD` value is assigned. Gas-reference applicability, COD/BOD activity-basis information, and a defensible relationship between reactor methane recovery and atmospheric release are not supplied by a mere change of units. The [unit policy](../../config/tidbrepo_unit_policy.json) remains the conversion gate. No quantitative scientific baseline, SQLite scientific record, or TIDBRepo entry is changed.

## Provenance and review files

- [[unverified-literature/20261028-september-source-review|Unverified source-checked extraction queue]]
- Curated, unverified proposals: `knowledge_base/literature_updates/curated/20261028-september-source-review.json`.
- Fresh local attempt: `knowledge_base/literature_updates/runs/20261028-september-source-review/`.
- `review.csv`: three rows, pending human decisions, with source-disagreement/correction notes.
- `source_checked_extraction.json`: source variants, exact evidence quotes, page/table locators, checksum, operating conditions, and the six Table 1 component observations.
- `automatic_proposals.jsonl`: unmodified output of the fresh deterministic extraction before the source correction.
- PDF, layout text, rendered source pages, screening gate, and manifest remain local.

The original September run and all of its files remain unchanged. The fresh attempt is manual source re-extraction, not a newly executed literature search, and does not generate a scheduled-run notification.

## Owner follow-up: R04 approved as wiki-only

On 28 October 2026, the owner approved retaining the corrected 56–66 mL CH4 batch range after 45 days with its individual conditions as wiki evidence. Conflicting continuous-production and yield figures remain explicitly unresolved. Reactor methane production/recovery is not a demonstrated atmospheric emission factor; no inventory-factor conversion or upload is authorized. The original proposals and review CSV remain unchanged as historical evidence.

The new context-only screening record is `knowledge_base/literature_updates/reviews/2026-10-28-suitability-R04.json`; the earlier retain/extract decision remains preserved. Quantitative verification status is unchanged.
