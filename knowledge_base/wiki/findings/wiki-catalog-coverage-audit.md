---
date: 2026-11-02
status: navigation-coverage-checked
---

# Paper catalog coverage and how to use it

The wiki home previously listed only 31 paper pages: the original 26-paper corpus and five reviewed monthly additions. Later screening and N02 upload decisions were recorded in review files but did not materialize paper pages or update the home list. This was a navigation/materialization gap, not evidence that the reviewed papers or approved database rows had been lost.

The repair creates 22 paper/source pages:

- N02: one owner-approved factor paper, with source evidence and TIDBRepo row IDs 181–183.
- Thirteen owner-retained context papers: four August entries, the September wastewater paper, and eight November entries. Retention alone does not approve their numeric results.
- Eight bibliographic pointers for DOI sources referenced by the database snapshot but absent from the original wiki. These are not full-text ingestions or source-verified measurement summaries.

[The complete catalog](../papers/index.md) now lists **53 distinct paper/source pages**. It covers all 14 latest retained monthly decisions and all 23 unique DOI source references in the independently verified 183-row snapshot after the N02 upload. The snapshot was captured on 1 November 2026; this is a recorded coverage check, not a continuously synchronized database mirror. The source registry and snapshot checksum are in `knowledge_base/reconciliations/wiki-source-registry.json`.

Official IPCC/BUR reports can lack DOIs; the 23-source figure counts DOI references only. It does not count every report citation or assert that all underlying full texts have been collected. Excluded and pending discoveries remain in [[unverified-literature/index|the discovery/decision archive]] rather than being silently promoted into retained literature.

## Using the wiki

1. Open `knowledge_base/wiki/` as an Obsidian vault, then open `index.md` and follow **Complete literature catalog**. You can also browse the files on GitHub; the complete catalog uses ordinary Markdown links that work on both GitHub and Obsidian. Older wiki pages still use Obsidian wikilinks.
2. Search by paper title, DOI, candidate ID or TIDBRepo row ID. A paper page links its review history and original source.
3. Check the status before using a finding: original machine-extracted notes, owner-retained context, approved factors and database-reference pointers are different evidence states.
4. For an LLM-assisted synthesis, supply the relevant paper pages and their review/source records. Metadata-only pages are useful for discovery, not sufficient to support detailed numerical claims. Obtain and inspect the source before extending them into quantitative evidence.

The source PDFs remain local. A paper page can be useful as a reference even when its full text is unavailable, but it cannot substitute for evidence that has not been ingested or checked.

## Preventing another gap

After recording owner paper decisions, run:

```bash
.venv/bin/python knowledge_base/pipeline/wiki_catalog.py
.venv/bin/python knowledge_base/pipeline/wiki_catalog.py --check
.venv/bin/python knowledge_base/pipeline/monthly_research.py validate-wiki
```

The catalog command creates only missing retained/reference notes, preserves existing paper text, and rebuilds navigation. It never approves measurements or uploads records. Wiki validation now checks that every paper page is listed, every retained decision and registered DOI source resolves to exactly one page, and the generated catalog is current. New discoveries continue to enter the unverified queue until the owner records a retention decision.

## Full-text follow-up, 2 November 2026

The eight bibliographic pointers described above have since been expanded into [source-checked full-text syntheses](database-source-synthesis-2026-11-02.md). The catalog still contains 53 distinct paper/source pages. Its new synthesis section distinguishes this evidence from metadata-only references and factor approvals. The earlier counts and descriptions above document the original catalog repair.
