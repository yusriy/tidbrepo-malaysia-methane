# TIDBRepo Malaysian methane literature-update workflow

This workflow searches for Malaysian methane values published after the retained 26 August 2023 search. It does not modify TIDBRepo, the frozen manuscript snapshot, or the local knowledge database during discovery, extraction, or review.

## Safety boundary

1. Internet results are candidates, not database records.
2. Only open-access PDFs are downloaded automatically.
3. Every proposed value retains DOI, source URL, PDF SHA-256, page, evidence quote, exact printed value/unit, and extraction rule.
4. Unit normalization and TIDBRepo classification require human review.
5. `prepare-upload` accepts only rows explicitly marked `approve` and rejects incomplete rows.
6. `upload` is a dry run unless `--execute` and the exact confirmation phrase are supplied together with a token.

## Commands

Run from the workspace root:

```bash
python knowledge_base/pipeline/tidbrepo_literature_update.py discover --mailto YOUR_EMAIL
python knowledge_base/pipeline/tidbrepo_literature_update.py extract knowledge_base/literature_updates/runs/RUN_ID
python knowledge_base/pipeline/tidbrepo_literature_update.py review knowledge_base/literature_updates/runs/RUN_ID
```

After a paper-level screening workbook has been reviewed, pass its recorded decision gate so only papers explicitly marked `retrieve_extract` are processed:

```bash
python knowledge_base/pipeline/tidbrepo_literature_update.py extract knowledge_base/literature_updates/runs/RUN_ID \
  --screening-decisions knowledge_base/literature_updates/runs/RUN_ID/screening_decisions.json
```

Automatic PDF extraction defaults to candidates scoring 8 or higher. Lower-scoring papers remain in `candidate_review.csv`; rerun extraction with `--minimum-score 6` after screening if one should be included.

## Unit standardization

Every value review must retain both the exact reported value/unit and a separate TIDBRepo-standardized value/unit. The conversion factor, formula, assumptions, and source locator must travel with the standardized value. Canonical units and approved direct conversions are defined in `knowledge_base/config/tidbrepo_unit_policy.json`.

Do not force a conversion when the activity denominator differs. Examples include POME surface flux versus kg CH4 per kg BOD, oil/gas volume-based factors versus kg CH4 per TJ, landfill BMP versus kg CH4 per kg total MSW, and percentage reductions without an absolute baseline. Such rows remain useful evidence but must be marked `not directly convertible` until the missing activity data are verified.

First review `candidate_review.csv` to decide which papers are in scope and which paywalled or failed sources should be retrieved manually. Then review `review.csv`: check the source page and evidence quote, classify the Malaysian sector/source/condition, record the appropriate statistic, and set the decision to `approve`, `reject`, or `needs_changes`.

Create a validated payload without uploading anything:

```bash
python knowledge_base/pipeline/tidbrepo_literature_update.py prepare-upload knowledge_base/literature_updates/runs/RUN_ID/review.csv
```

The uploader is intentionally not invoked by the normal workflow. Before its first use, confirm the authenticated TIDBRepo write endpoint and payload contract. The public read endpoint is not assumed to accept writes.

## Provenance chain

`OpenAlex record → OA source URL → frozen PDF checksum → page evidence → exact value/unit → reviewer decision → validated payload → upload receipt`

The search configuration is in `knowledge_base/config/tidbrepo_literature_update.json`. Each run freezes raw OpenAlex responses and records the configuration checksum in its manifest.
