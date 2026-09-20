# Factual-consistency audit

Status: working audit for manuscript revision  
Source manuscript: `2024 08 paper 1/manuscript_methane_v2_1.docx`  
Audit date: 25 August 2026

## Executive finding

The manuscript has a defensible central argument, but several numerical statements currently mix different denominators, datasets, observation systems, or evidence tiers. These issues should be corrected before language editing because they affect the abstract, results, discussion, figures, tables, and reviewer responses simultaneously.

## Critical corrections

### F01 — Included-study population is described inconsistently

**Current text**

- Abstract: “only 16 met strict empirical inclusion criteria.”
- Section 2.4: 21 studies met all inclusion criteria; 16 provided extractable emission factors or flux measurements.
- Sections 3, 6.1, and 7: repeatedly describe 16 as the full eligible set.

**Audit conclusion**

Use two explicitly named populations throughout:

- **21 studies in the qualitative evidence base**; and
- **16 studies in the quantitative synthesis with extractable CH₄ emission factors or fluxes**.

The abstract, Section 3, Table 1 caption, Section 6.1, summary, and PRISMA diagram must use the same terminology. If the authors instead intended only 16 studies to satisfy eligibility, Section 2.4 and the PRISMA diagram must be recomputed. The current text supports the 21/16 distinction.

**Status:** Ready to correct, subject to confirming the PRISMA counts.

### F02 — The reviewer’s “2003” cutoff is a reviewer typo, but the search period still needs documentation

The manuscript consistently states **2005–2023**, not 2003. The response should politely clarify this. However, the manuscript does not record:

- the final date on which each database was searched;
- why 2005 was the lower bound;
- why 31 December 2023, or another date in 2023, was the upper bound; or
- whether a 2024–2026 update search was conducted before revision.

**Required action:** Add the exact last-search date and a database-by-database search appendix. Decide whether to update the search through 2026 or justify retaining the protocol-defined 2023 cutoff.

**Status:** Author decision required.

### F03 — BUR4 inventory year is 2019

Malaysia submitted BUR4 on 31 December 2022, but the report states that its latest GHG inventory information extends through **2019**. All statements involving 1,420.98 Gg and 608.22 Gg should therefore specify “for the 2019 inventory reported in BUR4,” if those totals are confirmed against the analysis dataset.

Authoritative source: [Malaysia BUR4, UNFCCC](https://unfccc.int/sites/default/files/resource/MY%20BUR4_2022.pdf).

**Status:** Ready to correct year; totals still require recomputation.

### F04 — Emission-factor counts and emission volumes are different metrics

The current discussion interleaves:

- **306 emission-factor records/conditions**;
- **two country-specific factors**;
- **33.01% of factor records labelled Tier 1**;
- **1,420.98 Gg CH₄ attributed to Tier 1 calculations**; and
- **608.22 Gg CH₄ attributed to Tier 2 calculations**.

These metrics must be placed in separate subsections or panels:

1. **Factor availability/count:** number and percentage of factor records by tier/status.
2. **Emission magnitude:** Gg CH₄ calculated using each tier.

Do not infer inventory quality directly from record count without considering the emission magnitude represented by each record.

**Status:** Ready to restructure; underlying query must be archived.

### F05 — Tier comparison has the wrong direction

Section 5 states that Tier 1 AFOLU–Livestock emissions of **35.91 Gg CH₄ were lower than** Tier 2 emissions of **34.65 Gg CH₄**. Numerically, 35.91 is higher than 34.65 by 1.26 Gg, or approximately 3.6% relative to 34.65.

**Required action:** Change “lower” to “higher,” then verify whether the two values represent comparable scopes. The figure caption says Tier 1 excludes some cattle and Tier 2 covers enteric fermentation, suggesting that the scopes may differ; if so, a direct comparison may itself be invalid.

**Status:** Numerical error confirmed; scope confirmation required.

### F06 — The 12-year “national observational gap” is overstated

The manuscript says:

- 26 DOE stations stopped in 2010;
- four METMalaysia stations operated from 2022; and
- a NERC–UM station at Bachok has measured CH₄ since 2015.

Therefore, 2010–2022 may represent a gap in the **former DOE network**, but the manuscript’s own evidence does not support an absolute 12-year gap in all Malaysian CH₄ observations. Likewise, 26 DOE stations and four METMalaysia stations are not automatically comparable as a single network.

**Safer formulation:** “The cessation of the 26-station DOE programme in 2010 created a 12-year gap before the four-station METMalaysia programme began in 2022; other project or research observations, including Bachok from 2015, did not replace the former network’s national coverage.”

This wording still requires documentary support for network purpose, instrumentation, operating dates, and continuity.

**Status:** Overstatement confirmed; source verification required.

### F07 — Monitoring concentration is not the same as measuring emissions

Sections 1 and 4 move between ambient CH₄ concentration monitoring, surface-flux measurements, emission-factor development, and inventory validation. These are related but not interchangeable.

The revision should classify each network as one of:

- ambient concentration monitoring;
- ecosystem or surface-flux measurement;
- source/facility emission-rate measurement; or
- activity-data/inventory estimation.

The manuscript must not claim that fewer ambient concentration stations directly caused Tier 1 reliance without demonstrating a causal mechanism. At most, the network loss reduced independent atmospheric trend and validation capacity.

**Status:** Conceptual correction required.

### F08 — Gas chromatography is incorrectly treated as the source of sampling bias

Section 4 currently implies that ex-situ gas chromatography inherently underestimates emissions and contrasts it with a closed-chamber method described as in-situ and real-time. This conflates:

- the **sampling design**: chamber footprint, sampling interval, time of day, deployment duration, and treatment of ebullition; with
- the **analytical instrument**: GC-FID or another analyser used to quantify the collected sample.

GC can provide precise concentration analysis. Under-representation arises primarily when the field sampling design misses temporal or spatial variability. Closed chambers are not inherently real-time; they may be manual or automated and may feed different analysers.

**Status:** Ready for methodological rewrite.

### F09 — Method biases are overgeneralised

Statements that static chambers “typically underestimate” while eddy covariance, water sampling, and activity-data methods “could overpredict” are too categorical. Bias direction depends on deployment, footprint, turbulence correction, gap filling, transfer coefficients, chamber disturbance, frequency, and source heterogeneity.

**Required action:** Replace method-wide verdicts with a comparison of scale, temporal resolution, spatial footprint, detectable flux pathways, calibration, and uncertainty sources.

**Status:** Ready for methodological rewrite.

### F10 — Cattle emission-factor unit is wrong in Table 1

The cattle row reports **58.65 kg CH₄ ha⁻¹ yr⁻¹**. The underlying cattle paper reports animal-based factors (51.6 and 65.7 kg CH₄ animal⁻¹ yr⁻¹ for breeding cows and bulls); 58.65 appears to be their arithmetic mean. A hectare denominator is inappropriate.

**Required action:** Report the two sex-specific factors, or justify and label the averaged value as **58.65 kg CH₄ animal⁻¹ yr⁻¹**.

**Status:** Unit error confirmed.

### F11 — Energy units are incomplete

Energy rows and discussion use forms such as “0.9 kg CH₄ TJ” rather than **kg CH₄ TJ⁻¹**. Unit notation must be standardised in the table, text, and Figure 6.

**Status:** Ready to correct after checking the source table.

### F12 — Table structures are damaged

The Word table corresponding to the emission-factor summary contains blank reference cells, empty rows, inherited/merged labels, and displaced sector labels. The methodology table has a structurally inconsistent final row and several blank cells created by merges. This confirms Reviewer 2’s layout concern and makes row-level provenance ambiguous.

**Required action:** Rebuild both tables from a clean structured dataset; do not repair the current merged cells in place. Give every data row its own reference, sector, location/method, value, and unit.

**Status:** Rebuild required.

### F13 — The reported 306-factor count is not reproducibly tied to the working database

The manuscript states 306 factors. An earlier inspection of the TIDBRepo table reported 262 accessible rows. A live recheck on 25 August 2026 was blocked because the repository presented an expired TLS certificate, so the current public count could not be safely reverified.

Possible reasons include filters, multiple factor values per row, deleted/added records, or a different snapshot. The manuscript must cite a frozen export and transformation script that reproduces 306 exactly. The R script currently retrieves the live API and does not freeze the input.

**Status:** Critical data-reproducibility issue; frozen snapshot and recomputation required.

### F14 — The 44% energy/oil-and-gas share needs an exact denominator and source

The manuscript alternates among “oil and gas sector,” “energy sector,” “national emissions,” and “reported CH₄ emissions.” These are not interchangeable. The official BUR4 key-category discussion includes all greenhouse gases and different scopes; it does not by itself validate the manuscript’s 44% CH₄ statement.

**Required action:** Record the exact source table, inventory year, gas, unit, included subsectors, and denominator for 44%. If it is 44% of national CH₄ emissions in 2016 from another source, say so explicitly and do not present it as a BUR4 2019 value.

**Status:** Source confirmation required.

### F15 — CO₂-equivalent conversions need the GWP basis

The conversions 57.21 Mt CO₂-eq ≈ 2.04 Tg CH₄ and 3.05 Mt CO₂-eq ≈ 0.11 Tg CH₄ imply a GWP100 near 28. The manuscript should name the assessment report, fossil/biogenic convention if relevant, and time horizon. Do not mix conversions based on different GWP values.

**Status:** Source and convention confirmation required.

### F16 — Search reproducibility is incomplete

The manuscript lists databases and broad terms but does not preserve exact database-specific syntax, fields, dates, filters, or result counts. A supplementary search log should include:

- database/platform;
- exact query string;
- fields searched;
- search date;
- date/language/document filters;
- raw hits;
- export filename and checksum; and
- deduplication result.

**Status:** Supplement required; original search records needed from authors.

### F17 — Several assertions lack visible citations

Multiple sentences read “used…,” “established…,” or “performed…” without a displayed author citation. This may be caused by broken reference fields or missing citations. The problem is particularly visible in Sections 4 and 5.

**Required action:** Resolve citation fields, then check every methodological and quantitative statement against its source. Do not rely on the bibliography alone.

**Status:** Citation audit required.

### F18 — Minor but visible text defects

- “progressi2ve” in the abstract.
- “PRISM 2020” in Figure 1 caption should be “PRISMA 2020.”
- “Regulatory Constrains” should be “Regulatory Constraints.”
- Inconsistent CH₄/CH4, CO₂/CO2, hyphenation, and singular/plural forms.
- Numerous grammatical and missing-article errors.

**Status:** Correct after factual revisions, then perform a final language edit.

## Recommended factual sequence

1. Confirm the PRISMA population and exact search dates.
2. Freeze and checksum the TIDBRepo input used for all counts and figures.
3. Recompute factor counts, tier shares, emission totals, and sector shares from that snapshot.
4. Verify the station inventory from primary DOE, METMalaysia, and NERC–UM documentation.
5. Rebuild the two evidence tables from structured rows.
6. Rewrite the monitoring and methods sections with correct measurement distinctions.
7. Harmonise the abstract, results, Sections 6.1–6.2, and summary.
8. Only then complete language editing and reviewer responses.

