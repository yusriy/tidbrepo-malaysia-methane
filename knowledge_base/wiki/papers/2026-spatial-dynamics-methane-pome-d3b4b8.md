---
managed_by: "human-guided monthly literature workflow"
generated_kind: "curated paper evidence"
document_id: "monthly_candidate_d3b4b8d8fc03840a"
candidate_id: "candidate_d3b4b8d8fc03840a"
title: "Spatial dynamics of methane emissions and organic load reduction in a pond-based palm oil mill effluent treatment system"
year: 2026
doi: "10.1016/j.chemosphere.2026.144830"
manuscript_role: "monthly_literature_update"
verification_status: "human_value_review_complete"
tidbrepo_status: "wiki_only_activity_basis_incompatible"
---

# Spatial dynamics of methane emissions and organic load reduction in a pond-based palm oil mill effluent treatment system

> Verification status: five values were reviewed from the full paper and retained as Malaysian POME evidence. None is a new value on TIDBRepo's `kg CH4 kg-1 BOD` activity basis.

## Source record

- Evidence ID: `monthly_candidate_d3b4b8d8fc03840a`
- Candidate ID: `candidate_d3b4b8d8fc03840a`
- Authors: Takashi Onodera; Yoshiyuki Takahashi; Kazuya Nishina; Ryuichi Hirata; Joseph Wenceslaus Waili; Frankie Kiew; Guan Xhuan Wong; Lulie Melling
- Journal: *Chemosphere*
- Published: 2026
- DOI: https://doi.org/10.1016/j.chemosphere.2026.144830
- Local source: `knowledge_base/literature_updates/runs/2026-08-30-final/sources/candidate_d3b4b8d8fc03840a.pdf`
- SHA-256: `edb19a428540e61d8869e763e9e95a4607d402b7eadefed9ad0d9eb1916d360e`
- Pages: 9
- Review records: `MV-011A` through `MV-011E`

## Connections

- sector: [[topics/waste-sector|Waste sector]]
- system: [[topics/oil-palm-and-pome|Oil palm and POME]]
- location: [[locations/malaysia|Malaysia]]
- location: [[locations/sarawak|Sarawak]]
- theme: [[topics/methane-emission-factors|Methane emission factors]]
- review outcome: [[findings/monthly-value-review-2026-08-30|Monthly value review - 30 August 2026]]

## Study relevance

The study used floating chambers to characterize spatial and seasonal methane fluxes across a full-scale ten-pond POME treatment system in Sarawak. Pond 4 was an emission hotspot.

## Human-reviewed values

| Evidence ID | Metric and condition | Reported or reviewed value | Source locator | TIDBRepo disposition |
|---|---|---:|---|---|
| `MV-011A` | Pond 4 CH4 surface flux; 27–28 July 2018, dry season | 830 ± 570 µmol CH4 m-2 s-1 (`n=8`) | Table 2, PDF p. 4; Results p. 5 | Wiki context only. |
| `MV-011B` | Pond 4 CH4 surface flux; 28–29 January 2019, rainy season | 1000 ± 850 µmol CH4 m-2 s-1 (`n=5`) | Table 2, PDF p. 4; Results p. 5 | Wiki context only. |
| `MV-011C` | Pond 4 CH4 surface flux; 30 June–1 July 2019, dry season | 980 ± 420 µmol CH4 m-2 s-1 (`n=8`) | Table 2, PDF p. 4; Results p. 5 | Wiki context only. |
| `MV-011D` | Whole ten-pond system annual CH4 emission, reported on a carbon-mass basis | 2.79 Gg C yr-1 | Discussion, PDF p. 7 | Wiki context only; facility total, not an emission factor. |
| `MV-011E` | Existing Malaysian Tier 2 POME factor cited from Razak et al. (2023) | 0.225 kg CH4 kg-1 COD | Discussion, PDF p. 7 | Wiki context only; cited comparator and COD rather than BOD basis. |

## Interpretation and conversion boundary

- Surface flux can be converted to methane mass per area and time, but not to `kg CH4 kg-1 BOD` without contemporaneous BOD loading and a defensible area/throughput allocation.
- For `MV-011D`, multiplying by `16/12` would convert carbon mass to methane mass, but the result would remain a whole-facility annual total rather than an emission factor.
- `MV-011E` is already reported as methane mass, so the `16/12` carbon-to-methane conversion does not apply. It is also a cited comparator rather than a new measurement by this paper.

## Database status

- TIDBRepo upload: **No**
- Proposed category: `Wastewater Treatment and Discharge - Industrial`
- Canonical TIDBRepo unit: `kg CH4 kg-1 BOD`
- Main blocker: incompatible activity denominator or non-factor metric
- Scientific records in the SQLite knowledge database changed by this wiki addition: **No**

## Provenance chain

1. Local publisher PDF and SHA-256 checksum.
2. Page/table-level extraction recorded as `MV-011A` through `MV-011E`.
3. Researcher decision: `Wiki context only`.
4. Unit-policy assessment documenting why no BOD-based database factor can be derived.
5. Curated paper page: this file.
