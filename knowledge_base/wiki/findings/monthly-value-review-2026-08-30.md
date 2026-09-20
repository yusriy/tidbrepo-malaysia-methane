---
managed_by: "human-guided monthly literature workflow"
verification_status: "human_value_review_complete_crosswalk_pending"
run_id: "2026-08-30-final"
source_workbook_sha256: "01d7c8d67102b534247b53b7d3c22e94c2deb1a4035012c9af7bc09178a9288e"
---

# Monthly value review — 30 August 2026

The researcher completed every decision in the monthly value-extraction workbook. This page records the resulting wiki and TIDBRepo staging state; it is not an upload receipt.

## Human decision outcome

| Decision | Values |
|---|---:|
| Approve for wiki and TIDBRepo staging | 55 |
| Wiki context only | 11 |
| Unresolved | 0 |

The 11 context-only rows remain useful literature evidence but are excluded from the proposed TIDBRepo payload.

## Conservative TIDBRepo crosswalk

| Staging result | Values | Meaning |
|---|---:|---|
| Uploaded AFOLU and adjacent aquatic evidence | 41 | Rows 140–180 comprise three cattle, seven rice, 22 peat/land, and nine disturbed reservoir/river records. |
| Uploaded with sales-volume-labeled unit | 8 | Rows 132–139 use `kg CH4 m-3 oil sales volume` or `kg CH4 m-3 natural gas sales volume`; reported values and conversion formulas remain in the provenance package. |
| Staged with blockers | 6 | Landfill evidence is retained but cannot be represented in `kg CH4 kg-1 total MSW` without additional activity-basis data; one row is a rate constant rather than an emission factor. |
| Wiki context | 11 | Deliberately excluded from database staging by the researcher. |

The mature male, mature female, and pooled Kedah–Kelantan cross cattle emission factors from DOI `10.1051/e3sconf/202459901005` were uploaded on 20 September 2026 as TIDBRepo rows 140–142. Existing row 78 is an older Other Cattle Tier 2 range and remains a distinct representation rather than being replaced. A further 38 Malaysia-specific values from seven papers were uploaded as rows 143–180: seven Rice Cultivation records, 22 Peat lands records, and nine Disturbed river basins records from the anthropogenically influenced Kenyir Reservoir–Terengganu River–estuary system. All use Tier 2 and the canonical `kg CH4 ha-1 day-1` unit. The aquatic crosswalk is supported by documented dam discharge, sand extraction, and urban-runoff influences.

The eight energy records are the Malaysia-specific oil-and-gas factors from DOI `10.61762/pajevol10iss2art001`. They were uploaded on 20 September 2026 as TIDBRepo rows 132–139 and subsequently normalized to a mass-per-volume basis. Oil rows use `kg CH4 m-3 oil sales volume`; natural-gas rows use `kg CH4 m-3 natural gas sales volume`. For factors reported per `10^6 m3`, the numerical value is unchanged because `1 Gg = 10^6 kg`; the oil-production factor reported per `10^3 m3` was multiplied by 1000, from `1.11 × 10^-7` to `1.11 × 10^-4 kg CH4 m-3`.

## Blocker summary

| Blocker | Affected staged values | Resolution |
|---|---:|---|
| Tier confirmation | 6 | Applies only to the landfill records that remain blocked for a more fundamental activity-basis reason. |
| Category crosswalk | 0 | Rice, peat/land, and disturbed reservoir/river crosswalks were resolved for rows 143–180. |
| Unit or activity basis | 6 | Retain the landfill values as wiki evidence unless the missing total-MSW denominator and required physical conversion data become available. |

The oil-and-gas factors remain blocked only from conversion to the database's usual `kg CH4 TJ-1` basis because the paper reports mass per activity volume and supplies no matching source-specific net calorific value. They are stored under a documented mass-per-volume exception and must not be compared directly with `kg CH4 TJ-1` records. Landfill laboratory/model parameters likewise cannot be silently converted to `kg CH4 kg-1 total MSW`.

The context-only and blocked records are documented on dedicated paper pages:

- [[papers/2025-development-national-emission-factor-rice-malaysia-7e8229|Development of National Emission Factor for Rice Production System in Malaysia]] — the previously used regional comparator (`MV-002`).
- [[papers/2026-spatial-dynamics-methane-pome-d3b4b8|Spatial dynamics of methane emissions and organic load reduction in a pond-based POME treatment system]] — surface fluxes, a facility total, and a cited COD-based comparator (`MV-011A`–`MV-011E`).
- [[papers/2024-methane-nitrous-oxide-soil-stems-malaysian-peat-a77001|Methane and Nitrous Oxide Fluxes in Soil and Stems of Malaysian Tropical Peat Swamp Forest]] — conference-abstract evidence (`MV-025`–`MV-027`).
- [[papers/2024-rice-water-management-methane-3a6645|Plant Physiological Performances, Plant Growth, Grain Yield and Methane Emission of Rice in Response to Water Management]] — percentage reductions whose absolute factors are already uploaded (`MV-028`–`MV-029`).
- [[papers/2025-estimating-landfill-methane-emissions-shah-alam-1ef46a|Estimating Landfill Methane Emissions Based on Climatic Conditions and Major Waste Components in Shah Alam, Selangor, Malaysia]] — six activity-basis-blocked landfill values (`MV-014`–`MV-019`).

## Provenance artifacts

- `knowledge_base/literature_updates/runs/2026-08-30-final/wiki_staging/manifest.json`
- `knowledge_base/literature_updates/runs/2026-08-30-final/wiki_staging/reviewed_values.jsonl`
- `knowledge_base/literature_updates/runs/2026-08-30-final/wiki_staging/tidbrepo_comparison.csv`
- `knowledge_base/literature_updates/runs/2026-08-30-final/wiki_staging/tidbrepo_payload_preview.json`
- `knowledge_base/literature_updates/runs/2026-08-30-final/wiki_staging/energy_original_unit_upload_notes.json`
- `knowledge_base/literature_updates/runs/2026-08-30-final/wiki_staging/tidbrepo_energy_upload_receipt.json`
- `knowledge_base/snapshots/tidbrepo/methane_emission_factor_2026-09-20.json`
- `knowledge_base/literature_updates/runs/2026-08-30-final/wiki_staging/tidbrepo_energy_unit_normalization_receipt.json`
- `knowledge_base/snapshots/tidbrepo/methane_emission_factor_2026-09-20_volume_normalized.json`
- `knowledge_base/literature_updates/runs/2026-08-30-final/wiki_staging/tidbrepo_energy_sales_volume_label_receipt.json`
- `knowledge_base/snapshots/tidbrepo/methane_emission_factor_2026-09-20_sales_volume_labeled.json`
- `knowledge_base/literature_updates/runs/2026-08-30-final/wiki_staging/tidbrepo_cattle_upload_receipt.json`
- `knowledge_base/snapshots/tidbrepo/methane_emission_factor_2026-09-20_afolu_cattle_added.json`
- `knowledge_base/literature_updates/runs/2026-08-30-final/wiki_staging/tidbrepo_afolu_batch_upload_receipt.json`
- `knowledge_base/snapshots/tidbrepo/methane_emission_factor_2026-09-20_afolu_batch_added.json`

Each staged record retains the workbook checksum, review-row ID, candidate ID, DOI, local source checksum where available, page/table locator, evidence note, reviewed value and unit, proposed crosswalk, normalization rule, human decision, and comparison with the retained 28 August 2026 TIDBRepo representation.

## Safety status

- TIDBRepo records changed: **49 new rows (IDs 132–180)**
- SQLite scientific records changed: **0**
- Upload performed: **Yes—20 September 2026 over verified HTTPS**
- Oil-and-gas upload state: **Complete; eight records explicitly identify oil or natural-gas sales volume in the unit label and retain DOI `10.61762/pajevol10iss2art001`.**
- Upload attempt on 2 September 2026: **Blocked before transmission because `tidbrepo.usm.my` presented an invalid-date HTTPS certificate; no API token or confirmed authenticated write endpoint was available.**
- Upload on 20 September 2026: **Complete and independently verified from the public table; live table count increased from 131 to 139.**
- Unit normalization on 20 September 2026: **Complete and independently verified for rows 132–139; row 136 was correctly multiplied by 1000.**
- Sales-volume labeling on 20 September 2026: **Complete and independently verified for all eight records; numerical values and DOI fields were unchanged.**
- AFOLU cattle upload on 20 September 2026: **Complete and independently verified for rows 140–142; all three retain DOI `10.1051/e3sconf/202459901005`.**
- Remaining AFOLU batch upload on 20 September 2026: **Complete and independently verified for rows 143–180; the recovery verifier inserted no duplicate rows.**
- Current live TIDBRepo row count after the energy and AFOLU additions: **180.**
- Manuscript reproducibility boundary: **The frozen 28 August 2026 manuscript snapshot was not changed.**
- Next gate: keep the six landfill records in the wiki unless source-supported total-MSW activity-basis data make a valid database conversion possible.
