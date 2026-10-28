# Monthly methane factor plausibility report

The separate monthly Codex audit is scheduled for the **2nd at 09:00 Asia/Makassar (WITA)**. It reads the public database and emails a self-contained HTML report, with scientific comparison plots, from admin.atmosfera@gmail.com to yusriy@usm.my. It does not change the database, literature verification status, or the discovery systemd timer.

Run a fresh audit:

```sh
.venv/bin/python -m pip install -r knowledge_base/requirements-audit.txt
.venv/bin/python knowledge_base/pipeline/factor_plausibility.py --run-id YYYYMM-monthly
```

The command uses public GET requests, follows zero-based pagination until an empty terminal page, rejects duplicate IDs, and fails rather than silently using a stale snapshot. `--snapshot PATH` is an explicit offline option and is identified in provenance. Existing run IDs are immutable. There are no database write endpoints or credentials in this helper.

Complete snapshots and mail receipts remain in ignored `knowledge_base/plausibility_audits/runs/`. Curated HTML, Markdown, JSON findings, and PNG charts are in `knowledge_base/reports/plausibility/`. These preserve record IDs, original statistics, reported units, normalization formulae and DOI/source provenance. Published source references and original evidence remain unchanged. The API usually does not supply evidence quotes or table locators: follow the DOI and consult the existing evidence archive before making scientific decisions.

Plots compare categories with identical normalized units, displaying means and medians separately, with endpoints/ranges as recorded. Endpoints are never interpreted as means or confidence intervals. Annual area fluxes are divided by 365; other activity bases stay separate. Signed fluxes are retained. A 100-fold category span is contextual, not a physical plausibility rule. Species, processes and boundaries can explain it. Near-zero denominators can make ratios misleading.

Exploratory modified z scores on positive log10 values require exact matching country, condition and statistic, six peer rows and three independent source groups. Sources contribute equal-weight medians; candidate sources and overlapping DOIs are excluded. Different source labels do not guarantee independence. Groups with inadequate peers or zero MAD are marked unassessed. No statistical signal or numerical consistency issue establishes a source error; no signal establishes plausibility. Previously closed Q01/Q02 decisions are not automatically reopened. [NIST methodology](https://itl.nist.gov/div898/handbook/eda/section3/eda35h.htm).

Before email delivery, visually inspect charts and confirm the connected Gmail account. Claim exactly once:

```sh
.venv/bin/python knowledge_base/pipeline/factor_audit_mail.py claim YYYYMM-monthly
```

Send only to yusriy@usm.my, with the report attached as HTML (its plots are embedded). After a confirmed Gmail send, record the actual returned message ID:

```sh
.venv/bin/python knowledge_base/pipeline/factor_audit_mail.py ack YYYYMM-monthly --message-id ACTUAL_ID
```

Existing `mail.json` prevents a second claim. A `sending` state means delivery may be ambiguous: reconcile Gmail before retrying, report the run ID once, and record `attention_notified_at` locally. Never acknowledge an unconfirmed send. Receipts and raw snapshots must not be committed or emailed. The report attachment contains curated factor metadata, not raw API responses or papers.

Run unit tests and wiki validation before publishing curated reports on a development branch. Push and open a PR; merging into main still requires the owner's approval. A local Codex schedule requires the laptop and connected services to be available; delivery failures require attention rather than automatic resends.

## Accepted default convention and DOI maintenance

The owner accepts IPCC/BUR defaults stored only in `min`. The audit preserves that column and labels such IPCC records as default point factors, rather than measured minima or statistical means. This convention is not applied to literature records or min/max ranges. Official IPCC report citations do not require a journal DOI; preserve edition/chapter/table locators instead. Source-checked coal classification/unit proposals remain separate from authorized formatting changes.

DOI identities in matching and new upload payloads use lowercase bare DOIs; report hyperlinks use exactly one `https://doi.org/` prefix. Original forms are retained in provenance. The one-time, owner-authorized `normalize_tidbrepo_dois.py` updater uses a frozen DOI-only plan, conditional PUTs, a complete local backup and exact table read-back after each change. Without `--execute`, it is a public read-only dry run. With `--execute`, it prompts locally for a hidden, unsaved password; interrupted or ambiguous attempts cannot retry automatically. It never edits factors, units, source URLs or the proposed coal classifications.

If a DOI execution is interrupted, `normalize_tidbrepo_dois.py --reconcile` is a **read-only** operation: it compares the live table to the original backup and every permitted DOI-only result. It refuses unexpected changes. Only after successful reconciliation can a separate explicit `--execute` resume the pending rows; completed rows are skipped. The original backup and earlier failed receipt remain preserved. Authentication is used only for access checking and PUTs; public GETs verify the full table after each change. No write is retried automatically on HTTP 401 or ambiguous responses.
