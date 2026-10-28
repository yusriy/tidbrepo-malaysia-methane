# Original corpus matched against TIDBRepo — 28 October 2026

The original corpus is not a backlog of 95 missing uploads. All **96 local extracts from 18 papers** were compared with **180 live TIDBRepo rows**. The live rows agree with the saved 20 September snapshot after numeric formatting normalization. Eleven papers are already cited (ten by DOI, cattle by the source-title URL). A paper citation establishes source inclusion, not an exact match to every local extract.

The local `proposed` flags describe scientific verification of machine extracts; they do **not** describe upload status. Original records, statuses and evidence were preserved. No TIDBRepo records were changed.

## Numeric matches

| Paper / condition | Original value | Existing row / field | Normalized value |
|---|---|---|---|
| Methane fluxes from three ecosystems in tropical peatland of Sarawak, Malaysia | 15.14 mg C m | 99 / min | -0.0005530593607 kg CH₄ ha⁻¹ day⁻¹ |
| Local emission factors estimates for methane emission from cattle enteric fermentation using IPCC tier-2 methodology | 58.65 kg CH 4/animal/year | 78 / mean | 58.65 kg CH₄ head⁻¹ yr⁻¹ |
| Local emission factors estimates for methane emission from cattle enteric fermentation using IPCC tier-2 methodology | 65.7 kg CH 4/animal/year | 78 / max | 65.7 kg CH₄ head⁻¹ yr⁻¹ |
| Soil CO2 and CH4 fluxes from different forest types in tropical peat swamp forest | 1.74 g C m −2 yr−1 | 101 / mean | 0.06356164384 kg CH₄ ha⁻¹ day⁻¹ |
| Soil CO2 and CH4 fluxes from different forest types in tropical peat swamp forest | 7.39 g C m −2 yr−1 | 103 / mean | 0.2699543379 kg CH₄ ha⁻¹ day⁻¹ |
| Soil CO2 and CH4 fluxes from different forest types in tropical peat swamp forest | 4.20 g C m −2 yr−1 | 102 / mean | 0.1534246575 kg CH₄ ha⁻¹ day⁻¹ |

Six values match at stored precision after unit conversion. The Melling uptake requires restoring the negative sign lost by OCR. Three Busman forest means require converting CH4-C to CH4 mass using 16/12 and annual to daily using 365 days. These are reconciliation results, not new scientific approvals. The cattle paper’s 47 is a separate IPCC comparator already in row 77.

## Paper coverage

| Paper | Local extracts | Existing citation rows |
|---|---|---|
| Methane fluxes from three ecosystems in tropical peatland of Sarawak, Malaysia | 17 | 97, 99 |
| Comparison of Methane Emission from Conventional and Modified Paddy Cultivation in Malaysia | 2 | 109, 110, 111 |
| Local emission factors estimates for methane emission from cattle enteric fermentation using IPCC tier-2 methodology | 3 | 78 |
| Methane emissions from paddy cultivation and livestock farming in Sarawak, Malaysia | 13 | No citation match established |
| In Situ Tropical Peatland Fire Emission Factors and Their Variability, as Determined by Field Measurements in Peninsula Malaysia | 2 | 107 |
| Micrometeorological measurement of methane flux above a tropical peat swamp forest | 9 | No citation match established |
| Are secondary forests second-rate? Comparing peatland greenhouse gas emissions, chemical and microbial community properties between primary and secondary forests in Peninsular Malaysia | 1 | No citation match established |
| Carbon Dioxide and Methane Emissions from Peat Soil in an Undrained Tropical Peat Swamp Forest | 2 | No citation match established |
| Nitrous oxide (N2O) and methane (CH4) in rivers and estuaries of northwestern Borneo | 15 | 114, 115 |
| Greenhouse gas emissions resulting from conversion of peat swamp forest to oil palm plantation | 3 | 99 |
| How do land use practices affect methane emissions from tropical peat ecosystems? | 1 | 99 |
| Comparing GHG Emissions from Drained Oil Palm and Recovering Tropical Peatland Forests in Malaysia | 5 | 99 |
| Implications of municipal solid waste management on greenhouse gas emissions in Malaysia and the way forward | 2 | No citation match established |
| Water Table Fluctuation and Methane Emission in Pineapples (Ananas comosus (L.) Merr.) Cultivated on a Tropical Peatland | 1 | 95 |
| Mapping Trends of Carbon Dioxide and Methane During Movement Control Order in Industrial Areas in Peninsular Malaysia Using GOSAT, GOSAT-2, OCO-2, OCO-3, and TROPOMI Satellites Data | 6 | No citation match established |
| Soil CO2 and CH4 fluxes from different forest types in tropical peat swamp forest | 10 | 101, 102, 103 |
| Assessment of differences in peat physico-chemical properties, surface subsidence and GHG emissions between the major land-uses of Selangor peatlands | 2 | 95 |
| Rekod Jangka Panjang Kepekatan Metana di Malaysia (Long Term Record of Methane in Malaysia) | 2 | No citation match established |

## Focused checks remaining

- **Melling sago, row 97:** source 180 mg CH4-C m^-2 yr^-1 converts to 0.00657534 kg CH4 ha^-1 day^-1; stored 0.006559 differs by about 0.25%. Check original conversion and precision.
- **2014 paddy, rows 109/110:** extracted maxima 3.29 and 8.91 mg CH4 m^-2 day^-1 are different statistics/numbers from the database summaries. Check original tables, time basis and units before concluding a database error. Row 111 is an Indonesia comparator.
- **Three uncited flux papers:** eddy-covariance study (10.1016/j.agrformet.2018.03.025), secondary forest study (10.1016/j.scitotenv.2018.11.046), undrained peat study (10.1007/s10021-019-00376-8). Their flux records have no established same-condition match; determine whether they were intentionally excluded or covered elsewhere before proposing any upload.
- **Aggregated records 95/99:** Luta, Wong and recovering-forest oil-palm values have source citations in combined ranges, but individual contribution cannot be proven from range containment. Other forest conditions in cited papers also need separate treatment.

## Disposition of every extract

| Disposition | Records |
|---|---|
| aggregate_citation_only | 3 |
| ambiguous_table_fragment | 1 |
| approximate_source_summary | 1 |
| citation_match_value_discrepancy | 2 |
| cited_comparator_context | 4 |
| concentration_context | 8 |
| condition_specific_flux_not_matched | 9 |
| distinct_flux_unresolved | 14 |
| ipcc_comparator_match | 1 |
| near_match_discrepancy | 1 |
| not_methane_measurement | 19 |
| numeric_match | 6 |
| ocr_fragment | 1 |
| regional_total_context | 15 |
| threshold_context | 1 |
| uncertainty_or_interval_endpoint | 10 |

The JSON audit at `knowledge_base/reconciliations/original-corpus-tidbrepo-2026-10-28.json` lists every measurement ID, unchanged original value and status, source filename/hash, DOI, page/chunk, evidence quote, citation rows and match rationale. It also preserves the relevant database row values and live-response hash. Full raw responses remain local.

Limit: the comparison uses existing extracted PDF text; original PDFs were not visually rechecked in this pass. Non-methane values, concentrations, regional totals, uncertainty bounds, comparator values and OCR fragments are not new methane emission factors awaiting approval. Unresolved means insufficient evidence of a match, not confirmed missing data.

## Owner suitability decisions — 28 October 2026

The owner approved the proposed R01–R04 suitability template with “I agree”. This records intended use and follow-up conditions, not numerical verification or upload approval. Original evidence and earlier decisions remain preserved.

| ID | Paper | Approved disposition | Follow-up |
|---|---|---|---|
| R01 | Micrometeorological measurement of methane flux above a tropical peat swamp forest | wiki_only_database_hold | Ecosystem-scale flux includes aboveground emissions. Check Table 2 and choose a defensible processing method before any database preparation. |
| R03 | Carbon Dioxide and Methane Emissions from Peat Soil in an Undrained Tropical Peat Swamp Forest | factor_candidate_pending_full_text_verification | Candidate for undrained tropical peat-swamp forest soil. Confirm uncertainty definition, sampling coverage, site conditions and carbon-mass basis before preparing a final entry. |
| R02 | Are secondary forests second-rate? Comparing peatland greenhouse gas emissions, chemical and microbial community properties between primary and secondary forests in Peninsular Malaysia | wiki_only_database_hold | Obtain exact full-text condition-specific means, uncertainty and sampling coverage. Preserve supported negative uptake and keep forest conditions separate. |
| R04 | Production of Methane and Hydrogen from Mild-Strength Industrial Wastewater | wiki_only | Reactor production/recovery is not a demonstrated atmospheric emission factor. Activity basis and release accounting are required for inventory-factor interpretation. |

R01 and R02 remain on hold for database use; R03 advances only as a candidate pending full-text verification; R04 is wiki-only. Q01 sago and Q02 paddy checks remain open. Decision records: `knowledge_base/reconciliations/reviews/2026-10-28-suitability-R*.json`.
