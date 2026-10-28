---
date: 2026-10-29
type: database-audit-method
status: exploratory-unverified
---

# Monthly factor plausibility audit

A separate read-only audit compares the existing database by category and compatible units. It is scheduled for the 2nd of each month at 09:00 WITA and emails yusriy@usm.my a report with comparison plots. It does not change scientific verification status or database values.

The initial audit examined 180 records in 43 category/unit groups. It found no basic numerical consistency prompts, 12 broad magnitude contrasts, and insufficient independent comparable peers for 220 stored statistics. No statistical outlier signals were established; this does not show that all factors are plausible.

[Initial report and plots](../../reports/plausibility/20261028T170725Z/report.html) · [Reproducible findings](../../reports/plausibility/20261028T170725Z/audit.json) · [Operation and safeguards](../../FACTOR_AUDIT.md).

Means and medians remain distinct. Reported bounds are not confidence intervals, and min-only records are not treated as mean factors. Positive values spanning large scales use logarithmic axes; signed fluxes remain visible. Unit normalization preserves activity bases; only annual area fluxes are converted to daily values using 365 days. Broad spans across different fuels, species, methods, seasons or boundaries are contextual review aids, not evidence of errors. Very large ratios involving near-zero fluxes need special care.

An exploratory peer signal requires matching condition, country and statistic, six peer rows and three independent source groups, excluding the candidate source and overlapping DOIs. Source medians receive equal weight. Positive values are screened using log10 modified z scores above 3.5 in absolute magnitude; insufficient peers or zero MAD remain unassessed. [NIST outlier guidance](https://itl.nist.gov/div898/handbook/eda/section3/eda35h.htm).

Follow DOI/source links and check original tables, units and measurement boundaries before making any scientific correction. Existing evidence and resolved Q01/Q02 decisions remain intact. Scientific findings enter the main evidence synthesis only after review; an audit flag is not a verified finding.

## Owner clarification and coal source check — 29 October 2026

The owner accepts the established convention of storing selected IPCC defaults used in Malaysian BUR reporting in `min`. This is not a data defect. IPCC-labeled min-only rows are now labeled **default factors**, distinct from measured minima or means; source values remain intact. Of the 112 min-only records, 110 carry the IPCC label, while rows 100 and 111 retain their existing literature classifications. IPCC report citations should use edition, chapter and table/page locators; a journal DOI is optional.

The [USM report](https://indtech.usm.my/index.php/research-details/reports/methane-in-malaysia), Appendix A, Table A-1, printed page 63, reproduces the existing mining-category and kg/TJ labels. The original [2006 IPCC guidance](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_4_Ch4_Fugitive_Emissions.pdf), Equations 4.1.3 and 4.1.7, instead identifies 10 as the low underground-mining default and 0.3 as the low surface-mining default, both in methane volume per tonne of coal. Propose explicit underground/surface conditions and native source units; retain numerical values. The low-default depth conditions describe applicability, not independently verified Malaysian mine depths. Category/unit proposals are not database changes or new scientific verification decisions.

DOI identity is standardized as a lowercase bare DOI, with resolver URLs constructed separately for links. Original DOI strings remain in provenance and historical snapshots. The authorized live formatting plan changes only DOI columns; it cannot alter measurements, units, categories, conditions, source URLs or verification status. See `knowledge_base/reconciliations/reviews/2026-10-29-doi-normalization.json` and `2026-10-29-default-convention-and-coal-proposals.json`.

The owner ran the DOI-only updater. Following a partial HTTP 401 interruption, a public read established that only rows 12/13 had changed; the attempt was reconciled before resuming. Final independent read-back confirms **27 DOI fields across 22 records normalized**, all **180 records** retained, all non-DOI fields unchanged, and rows 55/58 unchanged. No factor or scientific verification decision changed. The local original backup and receipts are preserved; the curated progress record contains only status and hashes.

## Owner superseded coal proposals — 29 October 2026

The owner clarified that the existing coal values were deliberately converted to standardize units and instructed that **kg CH4/TJ, numeric values and categories remain unchanged**. The earlier native-unit/category proposals are retained as historical source checks and are not actionable. The owner authorized only the description (`condition`) fields: row 55, “Underground coal mining - IPCC Tier 1 low default”; row 58, “Surface coal mining - IPCC Tier 1 low default”. This description-only update is prepared separately; live completion requires read-back confirmation. No conversion details are inferred from the clarification. Decision: `knowledge_base/reconciliations/reviews/2026-10-29-coal-description-update.json`.
