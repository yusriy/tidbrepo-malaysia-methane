# Human verification queue

> Nothing in this queue becomes verified merely because it was extracted or linked by an LLM.

## Monthly literature

See [[unverified-literature/index|Unverified monthly literature queue]] for machine-discovered candidates. These entries and extracted measurements remain unverified until scientific review.

October 2026: **0 pending paper reviews**. The owner [[findings/literature-review-hcc-2026-10-28|excluded the Hydrothermal Compost Catalyst paper]] on 28 October 2026. The older verification items below are separate from this completed monthly review.

August 2026: **0 pending paper-screening decisions**. The owner [[findings/august-2026-remaining-screening-review|approved all 32 saved suggestions]] on 28 October 2026: 4 context-only and 28 excluded. The 66 value-review decisions are already complete; six landfill records retain their existing activity-basis/conversion blockers.

September 2026: **0 pending paper-screening decisions; 3 measurement decisions pending**. The owner excluded S01 and retained S02 for extraction. See [[findings/september-2026-screening-and-extraction-review|the source-checked S03–S05 review]] for conflicting reported figures and the corrected batch range. The current local measurement review file is `knowledge_base/literature_updates/runs/20261028-september-source-review/review.csv`; the original September run remains archived unchanged.

## Queue summary

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
