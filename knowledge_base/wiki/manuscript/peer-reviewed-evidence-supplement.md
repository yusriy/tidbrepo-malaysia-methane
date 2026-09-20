---
verification_status: "curated_working_evidence"
reviewed_on: "2026-08-27"
---

# Peer-reviewed evidence supplement and human-review priorities

This supplement maps journal evidence to the editor/reviewer queries. Bibliographic metadata and publisher records were checked online. Local full-text page evidence is available for Topa et al. (2023). Online articles remain evidence candidates until the authors confirm that each interpretation and manuscript placement is appropriate.

## Ranked human-review queue

### P0 — must be resolved before submission

1. **Replace 26 historical DOE stations with 19 unless a primary record proves a different programme scope.** Topa et al. (2023), pp. 1359 and 1361, reports 19 DOE continuous automatic air-quality monitoring stations with CH₄ records from 2000–2009. It identifies a Teledyne API M4020 flame-ionisation detector, hourly recording, and periodic calibration. Evidence: `chk_e75355db86_0003` and `chk_e75355db86_0006`.
2. **Verify the original KASA (2020) table behind 44%.** Topa et al. (2023), p. 1360, reports oil-and-gas emissions of 25,308 Gg CO₂-eq, equal to 44% of CH₄ emissions, and attributes the number to KASA (2020). The journal paper supports careful secondary citation, but the exact inventory year, table, sector boundary, and denominator still require confirmation from KASA. Evidence: `chk_e75355db86_0005`.
3. **Do not combine unlike networks.** Peer-reviewed evidence located in this audit verifies the historical DOE dataset but does not independently verify four METMalaysia stations from 2022 or continuous NERC–UM/Bachok CH₄ operation from 2015. Obtain programme records, instrument/QA-QC documentation, and operation dates before retaining these counts.
4. **Retain the frozen-data requirements.** No journal article can reproduce the manuscript’s 386 → 21 → 16 screening path or the TIDBRepo values (306 factors and Gg totals). Those require raw search exports, a screening ledger, a versioned database export, and the transformation script.

### P1 — scientific interpretation to review closely

5. **Approve the multi-scale worldwide methods comparison.** Static chambers provide source-scale direct measurements but require application-specific performance checks (Williams et al., 2023). Eddy covariance provides continuous ecosystem-scale fluxes within a meteorological footprint. UAV approaches bridge site and facility scales but depend on wind and plume assumptions (Shaw et al., 2021). Aircraft mass-balance methods can quantify facility clusters or regions (Karion et al., 2013). Satellites provide repeated regional-to-point-source observations, with detectability and attribution varying by sensor and inversion design (Jacob et al., 2022).
6. **Approve the validation wording.** Atmospheric observations can independently test aggregate inventory patterns, but they do not by themselves generate source-specific emission factors. Higher-tier development still requires source measurements and activity data. Alvarez et al. (2018) demonstrates the value of integrating measurements across scales rather than treating top-down and bottom-up approaches as substitutes.
7. **Confirm that the energy-gap paragraph says what the evidence supports.** The 44% number refers specifically to oil-and-gas CH₄ emissions as reported secondarily by Topa et al. (2023), while the lone reviewed energy study concerns power generation. This supports an evidence-coverage mismatch; it does not allow power-plant measurements to represent fugitive oil-and-gas sources.

### P2 — framework and presentation choices

8. **Approve a FAIR, access-controlled data architecture.** Assign persistent identifiers to datasets and analytical snapshots; expose rich metadata and provenance publicly; store sensitive facility data in a controlled-access layer; and publish only approved aggregates. These design choices implement the findability, accessibility, interoperability, and reusability principles of Wilkinson et al. (2016) without implying that proprietary raw data must be open.
9. **Approve the phased roadmap.** A defensible sequence is: 0–2 years, freeze datasets and audit inventory/search provenance; 2–5 years, conduct priority source campaigns and develop country-specific factors; 5+ years, integrate source, tower, airborne/UAV, satellite, and modelling evidence with scheduled factor updates. Exact institutional owners and dates remain author decisions.

## Source-to-query map

| Source | Reviewer query addressed | What it supports | Important limitation |
|---|---|---|---|
| Topa et al. (2023), DOI 10.17576/jsm-2023-5205-03 | 44% reconciliation; DOE station history; station purpose/instrumentation | 19 DOE CAQM stations, 2000–2009; M4020/FID; hourly data; calibration; 25,308 Gg CO₂-eq (44%) attributed to KASA 2020 | KASA remains the primary source for 44%; does not verify METMalaysia/Bachok continuity |
| Williams et al. (2023), DOI 10.5194/amt-16-3421-2023 | Worldwide methods; chamber limitations | Controlled-release evaluation of static chambers | Application-specific; not a Malaysia field comparison |
| Shaw et al. (2021), DOI 10.1098/rsta.2020.0450 | Worldwide methods; UAVs | UAV quantification methods and assumptions | Review evidence; performance depends on platform and flux model |
| Karion et al. (2013), DOI 10.1002/grl.50811 | Worldwide methods; aircraft | Airborne regional mass-balance quantification | Case study; meteorological/boundary assumptions matter |
| Jacob et al. (2022), DOI 10.5194/acp-22-9617-2022 | Satellite/inverse methods; validation | Scale-dependent satellite quantification and inverse analysis | Cannot alone assign source-specific emission factors |
| Alvarez et al. (2018), DOI 10.1126/science.aar7204 | Energy-sector gap; top-down/bottom-up integration | Multi-scale synthesis for oil-and-gas methane | U.S. evidence is methodological, not a Malaysian emission estimate |
| Wilkinson et al. (2016), DOI 10.1038/sdata.2016.18 | Public-private data framework; roadmap | FAIR metadata, identifiers, provenance and reuse | Does not resolve legal/contractual access terms |

## Proposed manuscript synthesis

International practice is best represented as a nested measurement system rather than a ranking of one universally superior technique. Source-scale chambers and analysers support process attribution and emission-factor development; towers provide continuous footprint-scale fluxes; UAV and aircraft surveys quantify facilities or regions; and satellites plus inverse modelling test spatial patterns and larger-scale totals. Cross-scale agreement and transparent uncertainty are therefore the relevant standards for Malaysia, not replacement of all existing methods with one platform.

For the monitoring argument, use a constrained causal statement: loss of a network can reduce long-term atmospheric baseline and independent validation capacity, but it does not directly cause Tier 1 factor use. Tier progression requires source-specific measurements, activity data, documented QA/QC, and repeated comparison with independent atmospheric observations.

## References

- Alvarez, R. A., Zavala-Araiza, D., Lyon, D. R., et al. (2018). Assessment of methane emissions from the U.S. oil and gas supply chain. *Science*, 361, 186–188. https://doi.org/10.1126/science.aar7204
- Jacob, D. J., Varon, D. J., Cusworth, D. H., et al. (2022). Quantifying methane emissions from the global scale down to point sources using satellite observations of atmospheric methane. *Atmospheric Chemistry and Physics*, 22, 9617–9646. https://doi.org/10.5194/acp-22-9617-2022
- Karion, A., Sweeney, C., Pétron, G., et al. (2013). Methane emissions estimate from airborne measurements over a western United States natural gas field. *Geophysical Research Letters*, 40, 4393–4397. https://doi.org/10.1002/grl.50811
- Shaw, J. T., Shah, A., Yong, H., & Allen, G. (2021). Methods for quantifying methane emissions using unmanned aerial vehicles: A review. *Philosophical Transactions of the Royal Society A*, 379, 20200450. https://doi.org/10.1098/rsta.2020.0450
- Topa, M. R., Latif, M. T., Othman, M., et al. (2023). Rekod jangka panjang kepekatan metana di Malaysia (Long term record of methane in Malaysia). *Sains Malaysiana*, 52, 1359–1370. https://doi.org/10.17576/jsm-2023-5205-03
- Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018. https://doi.org/10.1038/sdata.2016.18
- Williams, J. P., El Hachem, K., & Kang, M. (2023). Controlled-release testing of the static chamber methodology for direct measurements of methane emissions. *Atmospheric Measurement Techniques*, 16, 3421–3435. https://doi.org/10.5194/amt-16-3421-2023
