# Deployment bundle contents

The Ubuntu archive contains only the material required for monthly candidate discovery, provenance-preserving review, duplicate suppression, and local wiki reference.

- `deploy/`: installer, monthly runner, user-level `systemd` service template, timer, and instructions.
- `knowledge_base/pipeline/tidbrepo_literature_update.py`: deterministic discovery, PDF extraction, review, and approval-gate workflow.
- `knowledge_base/config/`: search configuration and unit policy.
- `knowledge_base/database/methane.sqlite`: current knowledge database used to recognize the established corpus.
- `knowledge_base/snapshots/tidbrepo/methane_emission_factor_2026-09-20_afolu_batch_added.json`: verified 180-row TIDBRepo reference snapshot.
- `knowledge_base/literature_updates/runs/2026-08-30-final/candidates.jsonl`: prior candidate identities used to suppress repeat monthly results.
- `knowledge_base/literature_updates/runs/2026-08-30-final/manifest.json`: provenance for the seed candidate set.
- `knowledge_base/literature_updates/runs/2026-08-30-final/screening_decisions.json`: retained human paper-screening decisions.
- `knowledge_base/literature_updates/README.md`: workflow and safety boundary.
- `knowledge_base/wiki/`: current curated local wiki, including monthly additions.
- `knowledge_base/tests/`: focused workflow tests.

The archive deliberately excludes PDF source files, raw OpenAlex responses, manuscript files, TIDBRepo credentials, and upload receipts. New open-access PDFs are downloaded into each future run directory and remain local to the Ubuntu laptop.
