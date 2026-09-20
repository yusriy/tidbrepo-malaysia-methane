---
managed_by: "human-guided monthly literature workflow"
generated_kind: "curated paper evidence"
document_id: "monthly_candidate_216934de1a1ef46a"
candidate_id: "candidate_216934de1a1ef46a"
title: "Estimating Landfill Methane Emissions Based on Climatic Conditions and Major Waste Components in Shah Alam, Selangor, Malaysia"
year: 2025
doi: "10.46754/jssm.2025.11.004"
manuscript_role: "monthly_literature_update"
verification_status: "human_value_review_complete"
tidbrepo_status: "not_uploaded_activity_basis_blocked"
---

# Estimating Landfill Methane Emissions Based on Climatic Conditions and Major Waste Components in Shah Alam, Selangor, Malaysia

> Verification status: the six values below were reviewed by the researcher in the August 2026 monthly literature workflow. They are retained as wiki evidence but were not uploaded to TIDBRepo because their activity bases do not match the database representation.

## Source record

- Evidence ID: `monthly_candidate_216934de1a1ef46a`
- Candidate ID: `candidate_216934de1a1ef46a`
- Authors: Nurzulaifa Shaheera Erne Mohd Yasim; Faeiza Buyong; Arnis Asmat; Mohd Talib Latif
- Journal: *Journal of Sustainability Science and Management*, 20(11), 2339-2369
- Published: 15 November 2025
- DOI: https://doi.org/10.46754/jssm.2025.11.004
- Local source: `knowledge_base/literature_updates/runs/2026-08-30-final/sources/candidate_216934de1a1ef46a.pdf`
- SHA-256: `d27f91f4d1e3035cd3a2e88d881c5ebd4731c3414ce16b988efac3c5aa1372e3`
- Pages: 31
- Review records: `MV-014` through `MV-019`

## Connections

- sector: [[topics/waste-sector|Waste sector]]
- location: [[locations/malaysia|Malaysia]]
- location: [[locations/selangor|Selangor]]
- theme: [[topics/methane-emission-factors|Methane emission factors]]
- theme: [[topics/national-inventory-and-ipcc-tiers|National inventory and IPCC tiers]]
- review outcome: [[findings/monthly-value-review-2026-08-30|Monthly value review - 30 August 2026]]

## Study relevance

The study evaluates how Shah Alam waste composition, rainfall, and ambient temperature influence landfill methane generation. It reports laboratory biochemical methane potential results and localized first-order-decay model parameters intended to improve Malaysian landfill methane estimates.

## Human-reviewed values

| Evidence ID | Metric and condition | Reported value | Source locator | TIDBRepo disposition |
|---|---|---:|---|---|
| `MV-014` | Ultimate methane generation potential (`L0`); cooked food waste BMP | 328.39 ml CH4 g-1 VS | PDF pp. 1 and 9 | Wiki evidence only; volatile-solids basis is not total wet MSW. |
| `MV-015` | Total methane output; 100% paper waste at 25 C | 43.78 L kg-1 | PDF pp. 1 and 14 | Wiki evidence only; pure-paper experimental basis and gas-state conversion remain unresolved. |
| `MV-016` | Total methane output; 100% paper waste at 37 C | 91.27 L kg-1 | PDF pp. 1 and 14 | Wiki evidence only; pure-paper experimental basis and gas-state conversion remain unresolved. |
| `MV-017` | BMP; Shah Alam mixed-waste composition, Reactor H | 229.91 ml CH4 g-1 VS | PDF p. 9 | Wiki evidence only; requires a defensible VS-to-total-wet-MSW conversion. |
| `MV-018` | Localized landfill `L0`; Shah Alam waste composition and laboratory data | 59.38 m3 Mg-1 wet waste | PDF pp. 20 and 22 | Inventory/model parameter retained in the wiki; methane density at stated reference conditions is needed for mass conversion. |
| `MV-019` | Localized methane-generation rate constant `k`; Shah Alam climatic conditions | 0.078 yr-1 | PDF pp. 20 and 22 | Model rate constant, not a methane emission factor. |

## Interpretation and conversion boundary

- The reported values are scientifically relevant to Malaysian landfill modeling, so they remain part of the literature evidence base.
- `MV-014` and `MV-017` use a volatile-solids denominator. Conversion to `kg CH4 kg-1 total MSW` requires the applicable volatile-solids fraction of total wet waste and methane density at documented temperature and pressure.
- `MV-015` and `MV-016` apply to 100% paper-waste reactors rather than total mixed MSW. A methane-density conversion alone would not resolve that denominator mismatch.
- `MV-018` already uses wet-waste mass as its denominator, but conversion from methane volume to methane mass still requires documented gas reference conditions.
- `MV-019` should remain a model parameter and must not be presented as an emission factor.

## Database status

- TIDBRepo upload: **No**
- Exact DOI match in the pre-upload TIDBRepo comparison: **None**
- Proposed category: `Solid Waste Disposal`
- Canonical TIDBRepo unit: `kg CH4 kg-1 total MSW`
- Current blocker: `unit_or_activity_basis`
- Scientific records in the SQLite knowledge database changed by this wiki addition: **No**

## Provenance chain

1. Publisher PDF and SHA-256 checksum.
2. Page-level extraction recorded in `reviewed_values.jsonl` as `MV-014` to `MV-019`.
3. Researcher decision: `Approve for wiki + TIDBRepo staging`.
4. Unit-policy assessment: database normalization blocked because the required activity-basis or gas-state information is incomplete.
5. Curated paper page: this file.

