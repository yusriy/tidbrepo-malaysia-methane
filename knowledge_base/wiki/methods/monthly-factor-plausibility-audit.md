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
