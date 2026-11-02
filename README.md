# Malaysian Methane Research Knowledge Base

A research knowledge base and literature-monitoring workflow for methane emissions and emission factors relevant to Malaysia. It brings together source evidence, quantitative factor assessments, research gaps, an Obsidian-compatible wiki, and reviewed updates to [TIDBRepo](https://tidbrepo.usm.my/).

The original literature corpus, monthly discoveries, scientific review decisions, and database submission records are preserved separately. A discovered paper or automatically extracted number is a proposal until reviewed against its source.

## Start here

| Task | Guide or entry point |
|---|---|
| Browse all retained papers and source references | [Complete literature catalog](knowledge_base/wiki/papers/index.md) |
| Read the eight expanded database source syntheses | [Full-text synthesis guide](knowledge_base/wiki/findings/database-source-synthesis-2026-11-02.md) |
| Browse sectors, methods, locations and research gaps | [Wiki home](knowledge_base/wiki/index.md) |
| Find outstanding scientific review actions | [Review queue](knowledge_base/wiki/review-queue.md) |
| Browse monthly discoveries and recorded screening decisions | [Unverified literature queue](knowledge_base/wiki/unverified-literature/index.md) |
| Understand discovery, extraction and source verification | [Literature workflow](knowledge_base/literature_updates/README.md) |
| Check factor consistency and comparison plots | [Factor audit guide](knowledge_base/FACTOR_AUDIT.md) and [published reports](knowledge_base/reports/plausibility/) |
| Maintain the existing laptop automation | [Monthly automation and notifications](deploy/MONTHLY-EXTENSIONS.md) |
| Set up a separate Ubuntu installation | [Ubuntu deployment guide](deploy/README-UBUNTU.md) |

For Obsidian, open `knowledge_base/wiki/` as a vault. Internal wiki pages use `[[wikilinks]]`; GitHub shows the Markdown files but does not provide all Obsidian navigation features.

## Research workflow

1. **Discover:** query OpenAlex for literature published after the retained 26 August 2023 baseline, compare DOI/title/record identities against the local corpus, reference snapshot and earlier monthly candidates, and rank relevant results. Check the live database again before any submission.
2. **Screen papers:** prioritize Malaysian inventory factors, field methane fluxes and relevant inventory inputs such as maximum methane potential (B₀). Separate useful policy, cost and modelling context from quantitative factor assessment. Record exclusions with reasons and preserve earlier decisions.
3. **Verify sources:** check publication dates, study location, methods and source availability. OpenAlex metadata and Malaysian author affiliation alone do not establish publication year or Malaysian measurement applicability.
4. **Review values:** inspect the PDF page/table/figure and retain DOI or authoritative report citation, source URL, evidence quote, PDF checksum, original value and unit, statistic, conditions, uncertainty and provenance. Record any justified unit conversion separately.
5. **Publish reviewed research:** commit curated metadata, review decisions and validated wiki changes on a development branch. Obtain owner approval before merging into `main`.
6. **Submit database records separately:** suitability approval and upload authorization are recorded separately. Explicitly approved API operations use source-specific payload checks, duplicate checks and read-back verification. The scheduled literature run never uploads to TIDBRepo.

The current automated screening uses transparent, owner-informed rules. It does **not** call an LLM or train a model. The [workflow audit](knowledge_base/wiki/findings/october-2026-workflow-audit.md) describes the proposed LLM advisory stage; any future model advice must remain separate from scientific approval.

## Monthly automation

The existing Ubuntu user service calls `deploy/run_monthly.sh`, which takes a nonblocking lock and runs the monthly orchestrator. The configured discovery timer runs on the **first of each month at 03:15 local time**, with up to 45 minutes of random delay and persistent catch-up. Preserve the installed timer and schedule unless the owner approves a change.

Each run keeps a complete local package, including `candidate_review.csv`, `review.csv`, `REVIEW.md`, logs, source PDFs and raw responses. The latest run is identified by:

```text
knowledge_base/literature_updates/state/latest_run_path.txt
```

Successful discovery produces a clearly labelled unverified wiki queue. When Git synchronization is enabled, curated outputs are validated, tested and published on `codex/monthly-literature`; the publisher never merges into `main`. Failures retain local evidence and identify the failed stage.

Two separately configured desktop automations complement the systemd discovery service:

- **Daily notification check:** at 09:00 WITA, deliver pending run summaries through the connected Gmail account. Summaries include success/failure, screening and candidate counts, proposed measurements, manual-review items and review-file paths. No email is sent when nothing is pending.
- **Monthly factor audit:** on the second of each month at 09:00 WITA, compare the public database within compatible categories, units and statistical contexts, then prepare and email a report with plots. Outlier flags are prompts for investigation, not automatic corrections.

These desktop delivery/audit schedules require the laptop, app and relevant connections to be available. They are separate from the systemd timer. See the linked deployment and audit guides for delivery claims, receipts and interrupted-send reconciliation.

## Local environment and checks

For an existing installation, use its `.venv` and private configuration. **Do not rerun the installer to update documentation or code:** it can reinstall the timer and rewrite configuration.

For a new development checkout with Python 3 and virtual-environment support:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r knowledge_base/requirements.txt
# Additional plotting dependency, when running factor audits:
.venv/bin/python -m pip install -r knowledge_base/requirements-audit.txt
```

OpenAlex cursor discovery needs an activated API key. The helper uses a hidden prompt, verifies access and saves the key privately outside the repository:

```bash
.venv/bin/python knowledge_base/pipeline/configure_openalex.py
# Check an existing key without changing configuration:
.venv/bin/python knowledge_base/pipeline/configure_openalex.py --check
```

Run checks before committing research or pipeline changes:

```bash
.venv/bin/python -m unittest discover -s knowledge_base/tests -q
.venv/bin/python knowledge_base/pipeline/monthly_research.py validate-wiki
bash -n deploy/run_monthly.sh
git diff --check
```

Manual discovery/extraction commands are in the [literature guide](knowledge_base/literature_updates/README.md). Preserve original run directories and create separate attempts for reprocessing: extraction/review commands can replace their output files. Use a fresh run ID for each factor audit.

## Repository layout and data handling

| Path | Purpose |
|---|---|
| `knowledge_base/wiki/` | Obsidian-compatible papers, topics, methods, findings, gaps and review queues |
| `knowledge_base/literature_updates/curated/` | Selected discovery metadata and provenance-complete, unverified proposals |
| `knowledge_base/literature_updates/reviews/` | Owner screening decisions and their history |
| `knowledge_base/reconciliations/` | Source/database comparisons, factor assessments, staged records and curated completion records |
| `knowledge_base/reports/plausibility/` | Curated audit reports and scientific plots |
| `knowledge_base/database/` and `knowledge_base/snapshots/` | Retained research database and reference snapshots; not a live mirror of TIDBRepo |
| `knowledge_base/pipeline/` and `knowledge_base/config/` | Processing scripts, screening rules and unit policy |
| `knowledge_base/tests/` | Workflow, provenance, API safety and audit tests |
| `deploy/` | Runner and deployment documentation/templates |

Complete monthly runs, downloaded PDFs, large raw API responses, runtime state, full audit snapshots and detailed delivery/submission receipts stay local under ignored directories. Previously tracked historical evidence remains preserved. Git is **not** a backup of ignored local evidence: back it up separately. Never force-add credentials or raw processing packages.

Maintain original values, unit bases and research history. A methane-production yield or modelled baseline is not automatically a measured atmospheric emission factor. Existing standardized TIDBRepo units must not be changed merely to match a paper's presentation. IPCC/BUR defaults stored in `min` follow the owner's documented convention; official reports can use edition/chapter/table citations without a journal DOI.

Third-party paper redistribution rights are not assumed. Consult the original publisher or repository for access and reuse terms.

Wiki maintenance after editing retained notes:

```bash
.venv/bin/python knowledge_base/pipeline/wiki_catalog.py
.venv/bin/python knowledge_base/pipeline/wiki_maintenance.py
.venv/bin/python knowledge_base/pipeline/monthly_research.py validate-wiki
.venv/bin/python knowledge_base/pipeline/wiki_maintenance.py --check
```

See the [cleanup and maintenance guide](knowledge_base/wiki/findings/wiki-consistency-cleanup-2026-11-02.md). The maintenance report checks both Markdown and Obsidian links, duplicate identities and reachability. Editorial navigation links preserve scientific statuses; undocumented methods or study locations are omitted. Full metadata responses remain local.

Routine after every addition: scheduled queue publication now runs catalog refresh,
configured navigation upkeep and the complete wiki audit before tests and any
commit/push. Only curated outputs are staged. For manual retained-paper additions,
`wiki_catalog.py` performs the same refresh; `validate-wiki` also checks maintenance.
The **Wiki addition checks** GitHub workflow validates pull requests and relevant
pushes, so direct edits are checked too. Broken links, duplicate identities, stale
navigation/reports or provenance errors fail validation. Missing metadata and
unassigned topics are reported for editorial follow-up; facts and approvals are
never guessed. These changes take effect when PR #15 is merged and the merged code
is used by the existing service; no timer or schedule change is needed.
