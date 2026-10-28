---
document_id: "doc_9bf65262ead38a20"
title: "Micrometeorological measurement of methane flux above a tropical peat swamp forest"
year: 2018
doi: "10.1016/j.agrformet.2018.03.025"
manuscript_role: "quantitative_baseline"
tidbrepo_baseline_decision: "approve_existing_representation"
verification_status: "machine_extracted"
---

# Micrometeorological measurement of methane flux above a tropical peat swamp forest

> Verification status: machine-extracted; bibliographic details and section boundaries require human review.

## Source record

- Database ID: `doc_9bf65262ead38a20`
- Local source: `pdfs/2018_wong.pdf`
- SHA-256: `9bf65262ead38a20dec292839978ca39c422582b47cec552e0bee3683bd10ee9`
- Authors: Guan Xhuan Wong
- DOI: https://doi.org/10.1016/j.agrformet.2018.03.025
- Pages: 9
- Search chunks: 38
- Manuscript role: `quantitative_baseline`
- TIDBRepo baseline decision: `approve_existing_representation`

## Connections

- ecosystem: [[topics/tropical-peatland|Tropical peatland]]
- location: [[locations/malaysia|Malaysia]]
- location: [[locations/sarawak|Sarawak]]
- method: [[methods/eddy-covariance|Eddy covariance]]
- sector: [[topics/afolu|AFOLU]]
- Proposed claims: 3
- Verified measurements: 0
- Proposed measurements: 9

## Abstract

Tropical peat swamp forest is a unique ecosystem, in which both swamp forest and peat soil have coexisted over
millennia and accumulated a signi ﬁcant amount of soil carbon as peat. Owing to the huge soil carbon stock and
high groundwater level (GWL), tropical peatlands potentially represent a signi ﬁcant source of methane (CH 4)t o
the atmosphere. However, a few studies of CH 4 ﬂux by the soil chamber technique have reported that annual
CH4 emissions from tropical peat swamp forest were very low as compared to mid- and high-latitude peatlands.
Recently, it has been reported that some tree species growing in peat swamp forest emit CH 4 from their stems. It
is impossible to continuously measure ecosystem-scale CH 4 ﬂux including both soil and plant-mediated CH 4
emissions by the chamber technique. Thus, we have measured net ecosystem CH 4 exchange (FCH 4) above a
tropical peat swamp forest in Sarawak, Malaysia using the eddy covariance technique from February 2014 to
July 2015 (18 months). The mean ( ± 1 standard deviation) of half-hourly measured FCH
4 was
24.0 ± 42.2 nmol m – 2 s– 1. Monthly mean FCH 4 was always positive during the 18 months, even in the driest
month with mean GWL of – 30 cm. FCH4 was positively associated with GWL or soil moisture in a quadratic form.
Annual FCH 4 from March 2014 through February 2015 was 7.5 – 10.8 g C m– 2 yr– 1. The annual FCH 4 was much
higher than annual soil CH 4 emissions from tropical peatlands, because the FCH 4 included aboveground CH 4
emissions mainly from tree stems. However, the annual FCH 4 was relatively low in comparison with those
measured by the eddy covariance technique in mid- and high-latitude peatlands.

## Detected structure

| Type | Original heading | Pages | Characters |
|---|---|---:|---:|
| front_matter | - | 1 | 719 |
| keywords | Keywords: | 1 | 104 |
| abstract | ABSTRACT | 1 | 1690 |
| introduction | 1. Introduction | 1-2 | 6179 |
| methods | 2. Material and methods | 2-4 | 11949 |
| results | 3. Results | 5-6 | 6417 |
| discussion | 4. Discussion | 6 | 1950 |
| references | References | 6-7 | 8365 |
| conclusion | 5. Conclusions | 7 | 1354 |
| acknowledgements | Acknowledgements | 8 | 659 |
| references | References | 8-9 | 14084 |

## Research notes

<!-- Add verified synthesis through the ingestion/review workflow. -->

## Owner suitability review — 28 October 2026 (R01)

Approved disposition: **wiki_only_database_hold**.

Retain annual range 7.5–10.8 g CH4-C m^-2 yr^-1 with processing methods. Do not select the method-variant average 9.2 as a preferred factor.

Ecosystem-scale flux includes aboveground emissions. Check Table 2 and choose a defensible processing method before any database preparation.

Scientific measurement verification is unchanged. This is not approval to upload. See [[findings/original-corpus-tidbrepo-reconciliation-2026-10-28|the original-corpus reconciliation and owner decisions]].

## Guided factor assessment — 29 October 2026 (R01)

**Assessment recommendation (subsequently accepted for staging by the owner, pending visual table check):** prepare one ecosystem-scale factor candidate representing the authors' preferred processing-estimate range, **9.8–10.8 g CH4-C m^-2 yr^-1**, rather than the full sensitivity range 7.5–10.8 or the across-method average 9.2. Original PDF p. 6 (printed p. 358), Table 2 and section 3.5 explicitly prefer eddy flux with morning flushes included. The original table was checked in stored full-page text; the PDF was not visually rechecked in this assessment.

| Flux processing | Morning flush | Gap filling | Annual g CH4-C m^-2 yr^-1 | Role |
|---|---|---|---:|---|
| Eddy + storage | Included | MDV | 9.4 | Sensitivity variant |
| Eddy + storage | Included | MI | 9.7 | Sensitivity variant |
| Eddy + storage | Excluded | MI | 8.0 | Sensitivity variant |
| Eddy | Included | MDV | 9.8 | Author-preferred |
| Eddy | Included | MI | 10.8 | Author-preferred |
| Eddy | Excluded | MI | 7.5 | Sensitivity variant |

The candidate applies to undrained Alan Batu forest at Maludam, **whole-ecosystem** above-canopy exchange, March 2014–February 2015. MDV and MI are alternative ways to fill missing observations. The preferred variants retain 27% of measured data after filtering, so gap-filling dependence must stay visible. The endpoints describe **method estimates for the same period**, not observed minima/maxima, a confidence interval, or independent replicate measurements. Table 2's flux-time-series SD is not the SD of the annual integrated estimate.

The existing conversion `value × (16/12) × 10 / 365` gives about **0.358–0.395 kg CH4 ha^-1 day^-1** as an illustrative daily equivalent of the annual estimates. Carry unrounded values in provenance and apply source-appropriate precision before submission. If accepted, label the min/max fields as a processing-estimate range in the condition; leave mean, median and SD empty. Keep this separate from soil-only R03 row 181; do not add or pool the two as independent ecosystem totals.

**Owner choice:** accept this explicitly labeled ecosystem-scale range for candidate staging, keep wiki-only, or hold for visual Table 2 checking. No new approval or upload is recorded. Detailed assessment: `knowledge_base/reconciliations/r01-r02-factor-assessment-2026-10-29.json`.

## Owner decision and staged range — 29 October 2026

The owner instructed: “R01: stage the author-preferred range, pending visual table check.” One candidate is staged in `knowledge_base/reconciliations/staging/r01-author-preferred-range-2026-10-29.json`, retaining source bounds 9.8–10.8 g CH4-C m^-2 yr^-1, unrounded conversion, source-precision preview bounds 0.36–0.395 kg CH4 ha^-1 day^-1, and the explicit ecosystem-scale processing-estimate-range condition. Mean, median and SD remain empty. The candidate is **not ready for upload**: original Table 2 visual checking and final representation checks remain incomplete, and no upload approval was given. The original source/measurement verification flags are unchanged. Separate owner decision: `knowledge_base/reconciliations/reviews/2026-10-29-factor-decision-R01.json`.

## Scope clarification — 29 October 2026

The owner clarified that the active task concerns new papers from automated discovery. This 2018 paper is already in the original knowledge base. Its assessment and staged range are preserved as legacy history; further visual Table 2 checking is deferred and is not a monthly review requirement. The visual gate remains incomplete, and no upload is authorized. Scope record: `knowledge_base/reconciliations/reviews/2026-10-29-monthly-discovery-scope.json`.
