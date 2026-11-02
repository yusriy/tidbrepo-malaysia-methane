---
date: 2026-11-02
status: editorial-cleanup
---

# Wiki consistency cleanup

This pass addresses navigation, bibliographic completeness and current-status clarity across the retained wiki. Scientific verification flags, accepted database values and standardized units are preserved. Historical review files and source evidence remain intact.

## Changes

- Added an authoritative [current review-status summary](../review-queue.md), distinguished the removed legacy R03 row from later N02 row IDs, and labeled original extraction counts as historical.
- Filled five missing publication years from publisher-deposited metadata or the existing source review. The hydrology commentary is dated 2026; its DOI suffix is not its publication year.
- Checked the two missing DOIs. Neither is established from the sources inspected; fuller citations and the limits of each check are on the paper pages. No DOI was invented.
- Added explicit editorial navigation for all 27 paper pages outside the original 26-paper corpus, plus the original satellite-monitoring page that lacked a topic backlink. Links record whether their basis is source-checked text, an owner review or title-level context. Undocumented methods and study locations are not inferred.
- Distinguished the Brakmas cattle paper's oil-palm background discussion from POME emission-factor evidence.
- Refreshed topic, method and location indexes using distinct linked-paper counts. New aquatic, policy/economic and modeling pages support previously missing navigation.
- Added [source follow-ups](../research-gaps/source-evidence-follow-ups.md), including source disagreements, scaling boundaries and dataset-independence checks, while preserving historical reviewer statements.
- Replaced the stale September lint report with a reproducible [current report](../lint-report.md) covering both Markdown and Obsidian links, reachability, duplicate identities and remaining metadata gaps.

## Maintenance and provenance

The [navigation registry](../../reconciliations/wiki-navigation-2026-11-02.json) records explicit editorial connections; the [metadata ledger](../../reconciliations/wiki-metadata-cleanup-2026-11-02.json) records source URLs and checksums where raw metadata was downloaded. Full responses stay local in `knowledge_base/literature_updates/runs/20261102-wiki-cleanup/`.

Run these commands after updating retained pages or navigation assignments:

```bash
.venv/bin/python knowledge_base/pipeline/wiki_catalog.py
.venv/bin/python knowledge_base/pipeline/wiki_maintenance.py
.venv/bin/python knowledge_base/pipeline/monthly_research.py validate-wiki
.venv/bin/python knowledge_base/pipeline/wiki_maintenance.py --check
```

The maintenance command updates only its marked connection blocks, navigation indexes and lint report. It preserves other note text. These commands do not upload records or alter schedules. No automatic live-job configuration was changed in this cleanup.

## Validation

All 106 unit tests passed. Catalog validation passed for 53 paper/source pages and eight source syntheses; the refreshed maintenance audit covers 117 Markdown pages with zero broken local links, orphan pages or duplicate normalized DOI/title identities. All 53 paper pages have topic navigation; 30 have documented method links and 45 have location links. The only remaining missing metadata fields are the two explicitly unestablished DOIs. A comparison against merged main confirmed unchanged scientific/owner status metadata for every paper page.

## Routine checks after additions

At the owner's request, scheduled queue publication now runs catalog refresh and configured maintenance before validation, tests, commit and push. Its explicit curated-file list includes changed navigation and the lint report. Tests run against the publication checkout. For manual retained additions, `wiki_catalog.py` invokes the same upkeep; `validate-wiki` verifies the maintenance report. A read-only GitHub Actions workflow checks relevant pull requests and pushes, including direct wiki edits. Stale reports, duplicate identities and broken navigation block validation; metadata and topic-assignment gaps are reported without inventing scientific facts. No new schedule or TIDBRepo access is configured. This routine becomes active once the reviewed changes are merged and used by the existing service.

Validation after this follow-up: 110 unit tests passed, including configured repeated-addition upkeep, preservation of unverified proposal status, and rejection of broken navigation. Wiki validation passed for 117 pages.

The clean publication development checkout fast-forwards from merged `main` before additions so an older checkout cannot bypass the routine. A dirty or divergent checkout requires reconciliation; neither main nor owner edits are reset. A checkout without the merged maintenance configuration cannot publish.
