# Knowledge-base activity log

Append-only record of ingestion, compilation, queries, review imports, and lint passes.

## [2026-08-25T15:39:43Z] compile | Applied complete Karpathy-style workflow to the local corpus

```json
{
  "compiled": {
    "claims": 64,
    "measurements": 156,
    "papers": 25,
    "review_comments": 32,
    "topics": 23
  },
  "lint": {
    "broken_links": [
      "findings/index.md -> proposed-paper-findings",
      "findings/proposed-paper-findings.md -> papers/2005-methane-fluxes-from-three-ecosystems-in-tropical-peatland-of-sarawak-malaysia-2f1075",
      "findings/proposed-paper-findings.md -> papers/2005-methane-fluxes-from-three-ecosystems-in-tropical-peatland-of-sarawak-malaysia-31303c",
      "findings/proposed-paper-findings.md -> papers/2005-methane-fluxes-from-three-ecosystems-in-tropical-peatland-of-sarawak-malaysia-54942f",
      "findings/proposed-paper-findings.md -> papers/2014-comparison-of-methane-emission-from-conventional-and-modified-paddy-cultivation--322fca",
      "findings/proposed-paper-findings.md -> papers/2014-comparison-of-methane-emission-from-conventional-and-modified-paddy-cultivation--8d9a3f",
      "findings/proposed-paper-findings.md -> papers/2014-comparison-of-methane-emission-from-conventional-and-modified-paddy-cultivation--7f531e",
      "findings/proposed-paper-findings.md -> papers/2017-local-emission-factors-estimates-for-methane-emission-from-cattle-enteric-fermen-5c24fb",
      "findings/proposed-paper-findings.md -> papers/2017-local-emission-factors-estimates-for-methane-emission-from-cattle-enteric-fermen-0b619a",
      "findings/proposed-paper-findings.md -> papers/2017-local-emission-factors-estimates-for-methane-emission-from-cattle-enteric-fermen-01e147",
      "findings/proposed-paper-findings.md -> papers/2017-methane-emission-from-pineapple-cultivation-on-a-tropical-peatland-at-saratok-ma-084bee",
      "findings/proposed-paper-findings.md -> papers/2017-methane-emission-from-pineapple-cultivation-on-a-tropical-peatland-at-saratok-ma-b87485",
      "findings/proposed-paper-findings.md -> papers/2017-methane-emission-from-pineapple-cultivation-on-a-tropical-peatland-at-saratok-ma-7eb8e9",
      "findings/proposed-paper-findings.md -> papers/2017-methane-emissions-from-paddy-cultivation-and-livestock-farming-in-sarawak-malays-aee7ba",
      "findings/proposed-paper-findings.md -> papers/2017-methane-emissions-from-paddy-cultivation-and-livestock-farming-in-sarawak-malays-ca7039",
      "findings/proposed-paper-findings.md -> papers/2017-methane-emissions-from-paddy-cultivation-and-livestock-farming-in-sarawak-malays-0375a0",
      "findings/proposed-paper-findings.md -> papers/2018-in-situ-tropical-peatland-fire-emission-factors-and-their-variability-as-determi-c85046",
      "findings/proposed-paper-findings.md -> papers/2018-in-situ-tropical-peatland-fire-emission-factors-and-their-variability-as-determi-535f91",
      "findings/proposed-paper-findings.md -> papers/2018-in-situ-tropical-peatland-fire-emission-factors-and-their-variability-as-determi-bf9dcd",
      "findings/proposed-paper-findings.md -> papers/2018-micrometeorological-measurement-of-methane-flux-above-a-tropical-peat-swamp-fore-3bb4ab",
      "findings/proposed-paper-findings.md -> papers/2018-micrometeorological-measurement-of-methane-flux-above-a-tropical-peat-swamp-fore-8a402d",
      "findings/proposed-paper-findings.md -> papers/2018-micrometeorological-measurement-of-methane-flux-above-a-tropical-peat-swamp-fore-44efc0",
      "findings/proposed-paper-findings.md -> papers/2019-are-secondary-forests-second-rate-comparing-peatland-greenhouse-gas-emissions-ch-7ea246",
      "findings/proposed-paper-findings.md -> papers/2019-are-secondary-forests-second-rate-comparing-peatland-greenhouse-gas-emissions-ch-31d4bf",
      "findings/proposed-paper-findings.md -> papers/2019-are-secondary-forests-second-rate-comparing-peatland-greenhouse-gas-emissions-ch-7de57a",
      "findings/proposed-paper-findings.md -> papers/2019-carbon-dioxide-and-methane-emissions-from-peat-soil-in-an-undrained-tropical-pea-3070ba",
      "findings/proposed-paper-findings.md -> papers/2019-carbon-dioxide-and-methane-emissions-from-peat-soil-in-an-undrained-tropical-pea-dd07a9",
      "findings/proposed-paper-findings.md -> papers/2019-carbon-dioxide-and-methane-emissions-from-peat-soil-in-an-undrained-tropical-pea-753c1b",
      "findings/proposed-paper-findings.md -> papers/2019-nitrous-oxide-n2o-and-methane-ch4-in-rivers-and-estuaries-of-northwestern-borneo-1c0040",
      "findings/proposed-paper-findings.md -> papers/2019-nitrous-oxide-n2o-and-methane-ch4-in-rivers-and-estuaries-of-northwestern-borneo-6cb728",
      "findings/proposed-paper-findings.md -> papers/2019-nitrous-oxide-n2o-and-methane-ch4-in-rivers-and-estuaries-of-northwestern-borneo-f9dc8b",
      "findings/proposed-paper-findings.md -> papers/2020-greenhouse-gas-emissions-resulting-from-conversion-of-peat-swamp-forest-to-oil-p-803325",
      "findings/proposed-paper-findings.md -> papers/2020-greenhouse-gas-emissions-resulting-from-conversion-of-peat-swamp-forest-to-oil-p-3bcfa9",
      "findings/proposed-paper-findings.md -> papers/2020-greenhouse-gas-emissions-resulting-from-conversion-of-peat-swamp-forest-to-oil-p-0102be",
      "findings/proposed-paper-findings.md -> papers/2020-how-do-land-use-practices-affect-methane-emissions-from-tropical-peat-ecosystems-84561b",
      "findings/proposed-paper-findings.md -> papers/2020-how-do-land-use-practices-affect-methane-emissions-from-tropical-peat-ecosystems-f96a5b",
      "findings/proposed-paper-findings.md -> papers/2020-how-do-land-use-practices-affect-methane-emissions-from-tropical-peat-ecosystems-aa464a",
      "findings/proposed-paper-findings.md -> papers/2021-comparing-ghg-emissions-from-drained-oil-palm-and-recovering-tropical-peatland-f-ab0025",
      "findings/proposed-paper-findings.md -> papers/2021-comparing-ghg-emissions-from-drained-oil-palm-and-recovering-tropical-peatland-f-8547d1",
      "findings/proposed-paper-findings.md -> papers/2021-comparing-ghg-emissions-from-drained-oil-palm-and-recovering-tropical-peatland-f-00a551",
      "findings/proposed-paper-findings.md -> papers/2021-implications-of-municipal-solid-waste-management-on-greenhouse-gas-emissions-in--256b3c",
      "findings/proposed-paper-findings.md -> papers/2021-implications-of-municipal-solid-waste-management-on-greenhouse-gas-emissions-in--4aa80a",
      "findings/proposed-paper-findings.md -> papers/2022-impact-of-interannual-and-multidecadal-trends-on-methane-climate-feedbacks-and-s-aa79dd",
      "findings/proposed-paper-findings.md -> papers/2022-impact-of-interannual-and-multidecadal-trends-on-methane-climate-feedbacks-and-s-7f71bf",
      "findings/proposed-paper-findings.md -> papers/2022-impact-of-interannual-and-multidecadal-trends-on-methane-climate-feedbacks-and-s-f0212e",
      "findings/proposed-paper-findings.md -> papers/2022-mapping-trends-of-carbon-dioxide-and-methane-during-movement-control-order-in-in-43912c",
      "findings/proposed-paper-findings.md -> papers/2022-mapping-trends-of-carbon-dioxide-and-methane-during-movement-control-order-in-in-20338f",
      "findings/proposed-paper-findings.md -> papers/2022-mapping-trends-of-carbon-dioxide-and-methane-during-movement-control-order-in-in-08ea65",
      "findings/proposed-paper-findings.md -> papers/2022-soil-co2-and-ch4-fluxes-from-different-forest-types-in-tropical-peat-swamp-fores-2f6c17",
      "findings/proposed-paper-findings.md -> papers/2022-soil-co2-and-ch4-fluxes-from-different-forest-types-in-tropical-peat-swamp-fores-f34939",
      "findings/proposed-paper-findings.md -> papers/2022-soil-co2-and-ch4-fluxes-from-different-forest-types-in-tropical-peat-swamp-fores-d35ee1",
      "findings/proposed-paper-findings.md -> papers/2023-assessing-machine-learning-tools-for-methane-emission-prediction-from-pome-treat-f2a5fa",
      "findings/proposed-paper-findings.md -> papers/2023-assessing-machine-learning-tools-for-methane-emission-prediction-from-pome-treat-85b23e",
      "findings/proposed-paper-findings.md -> papers/2023-assessment-of-differences-in-peat-physico-chemical-properties-surface-subsidence-d26864",
      "findings/proposed-paper-findings.md -> papers/2023-assessment-of-differences-in-peat-physico-chemical-properties-surface-subsidence-56b95d",
      "findings/proposed-paper-findings.md -> papers/2023-assessment-of-differences-in-peat-physico-chemical-properties-surface-subsidence-0374ef",
      "findings/proposed-paper-findings.md -> papers/2023-mapping-of-greenhouse-gas-concentration-in-peninsular-malaysia-industrial-areas--7e29d3",
      "findings/proposed-paper-findings.md -> papers/2023-mapping-of-greenhouse-gas-concentration-in-peninsular-malaysia-industrial-areas--8a8fca",
      "findings/proposed-paper-findings.md -> papers/2023-mapping-of-greenhouse-gas-concentration-in-peninsular-malaysia-industrial-areas--a58721",
      "findings/proposed-paper-findings.md -> papers/2023-rekod-jangka-panjang-kepekatan-metana-di-malaysia-long-term-record-of-methane-in-8084d1",
      "findings/proposed-paper-findings.md -> papers/2023-rekod-jangka-panjang-kepekatan-metana-di-malaysia-long-term-record-of-methane-in-cee2f6",
      "findings/proposed-paper-findings.md -> papers/2023-rekod-jangka-panjang-kepekatan-metana-di-malaysia-long-term-record-of-methane-in-61d54c",
      "findings/proposed-paper-findings.md -> papers/2023-simultaneous-dissolved-methane-and-nitrogen-removal-from-low-strength-wastewater-1348d2",
      "findings/proposed-paper-findings.md -> papers/2023-simultaneous-dissolved-methane-and-nitrogen-removal-from-low-strength-wastewater-1a0b23",
      "findings/proposed-paper-findings.md -> papers/2023-simultaneous-dissolved-methane-and-nitrogen-removal-from-low-strength-wastewater-66e4bd",
      "locations/index.md -> malaysia",
      "locations/index.md -> peninsular-malaysia",
      "locations/index.md -> sabah",
      "locations/index.md -> sarawak",
      "locations/index.md -> selangor",
      "manuscript/index.md -> reviewer-response-workspace",
      "methods/index.md -> closed-chamber",
      "methods/index.md -> eddy-covariance",
      "methods/index.md -> gas-chromatography",
      "methods/index.md -> ipcc-inventory-calculation",
      "methods/index.md -> machine-learning",
      "methods/index.md -> satellite-remote-sensing",
      "methods/index.md -> uav-sensing",
      "topics/index.md -> livestock-and-enteric-fermentation",
      "topics/index.md -> oil-palm-and-pome",
      "topics/index.md -> paddy-and-rice-cultivation",
      "topics/index.md -> peat-and-biomass-fire",
      "topics/index.md -> tropical-peatland",
      "topics/index.md -> afolu",
      "topics/index.md -> energy-sector",
      "topics/index.md -> waste-sector",
      "topics/index.md -> atmospheric-methane-monitoring",
      "topics/index.md -> methane-emission-factors",
      "topics/index.md -> national-inventory-and-ipcc-tiers"
    ],
    "orphan_pages": [
      "findings/proposed-paper-findings.md",
      "manuscript/reviewer-response-workspace.md"
    ],
    "pages": 57
  },
  "proposed_claims": 64,
  "proposed_measurements": 156,
  "review_comments": 32,
  "topics": {
    "assignments": 221,
    "documents": 25,
    "topics": 23
  }
}
```

## [2026-08-25T15:40:09Z] compile | Regenerated interlinked wiki pages

```json
{
  "claims": 64,
  "measurements": 156,
  "papers": 25,
  "review_comments": 32,
  "topics": 23
}
```

## [2026-08-25T15:40:09Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 59
}
```

## [2026-08-25T15:41:23Z] compile | Applied complete Karpathy-style workflow to the local corpus

```json
{
  "compiled": {
    "claims": 64,
    "measurements": 95,
    "papers": 25,
    "review_comments": 32,
    "topics": 23
  },
  "lint": {
    "broken_links": [],
    "orphan_pages": [],
    "pages": 60
  },
  "proposed_claims": 64,
  "proposed_measurements": 95,
  "review_comments": 32,
  "topics": {
    "assignments": 149,
    "documents": 25,
    "topics": 23
  }
}
```

## [2026-08-25T15:41:23Z] query | Filed research query: Which methods were used to measure methane flux in the Malaysian studies?

```json
{
  "evidence_chunks": 10,
  "file": "/Users/yusriyusup/Documents/Codex_workspaces/methane_analysis/knowledge_base/wiki/findings/query-methane-measurement-methods-in-the-corpus.md"
}
```

## [2026-08-25T15:41:23Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 61
}
```

## [2026-08-25T15:41:48Z] query | Filed research query: What evidence documents the mismatch between energy-sector emissions and research coverage?

```json
{
  "evidence_chunks": 10,
  "file": "/Users/yusriyusup/Documents/Codex_workspaces/methane_analysis/knowledge_base/wiki/findings/query-energy-sector-evidence-and-research-coverage.md"
}
```

## [2026-08-25T15:41:51Z] compile | Regenerated interlinked wiki pages

```json
{
  "claims": 64,
  "measurements": 95,
  "papers": 25,
  "review_comments": 32,
  "topics": 23
}
```

## [2026-08-25T15:41:51Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 62
}
```

## [2026-08-25T15:42:02Z] query | Filed research query: Which methods were used to measure methane flux in the Malaysian studies?

```json
{
  "evidence_chunks": 12,
  "file": "/Users/yusriyusup/Documents/Codex_workspaces/methane_analysis/knowledge_base/wiki/findings/query-methane-measurement-methods-in-the-corpus.md"
}
```

## [2026-08-25T15:42:02Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 62
}
```

## [2026-08-25T15:43:21Z] compile | Applied complete Karpathy-style workflow to the local corpus

```json
{
  "compiled": {
    "claims": 64,
    "measurements": 95,
    "papers": 25,
    "review_comments": 32,
    "review_evidence_suggestions": 40,
    "topics": 23
  },
  "lint": {
    "broken_links": [],
    "orphan_pages": [],
    "pages": 63
  },
  "proposed_claims": 64,
  "proposed_measurements": 95,
  "review_comments": 32,
  "review_evidence_suggestions": 40,
  "topics": {
    "assignments": 149,
    "documents": 25,
    "topics": 23
  }
}
```

## [2026-08-25T15:43:21Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 63
}
```

## [2026-08-25T15:45:28Z] compile | Applied complete Karpathy-style workflow to the local corpus

```json
{
  "compiled": {
    "claims": 64,
    "measurements": 95,
    "papers": 25,
    "review_comments": 32,
    "review_evidence_suggestions": 40,
    "topics": 23
  },
  "lint": {
    "broken_links": [],
    "orphan_pages": [],
    "pages": 63
  },
  "proposed_claims": 64,
  "proposed_measurements": 95,
  "review_comments": 32,
  "review_evidence_suggestions": 40,
  "topics": {
    "assignments": 149,
    "documents": 25,
    "topics": 23
  }
}
```

## [2026-08-25T15:45:28Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 63
}
```

## [2026-08-25T15:45:59Z] compile | Regenerated interlinked wiki pages

```json
{
  "claims": 64,
  "measurements": 95,
  "papers": 25,
  "review_comments": 32,
  "review_evidence_suggestions": 40,
  "topics": 23
}
```

## [2026-08-25T15:45:59Z] compile | Regenerated interlinked wiki pages

```json
{
  "claims": 64,
  "measurements": 95,
  "papers": 25,
  "review_comments": 32,
  "review_evidence_suggestions": 40,
  "topics": 23
}
```

## [2026-08-25T15:45:59Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 64
}
```

## [2026-08-25T15:59:00Z] compile | Regenerated interlinked wiki pages

```json
{
  "claims": 64,
  "measurements": 95,
  "papers": 25,
  "review_comments": 32,
  "review_evidence_suggestions": 40,
  "topics": 23
}
```

## [2026-08-25T15:59:04Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 66
}
```

## [2026-08-26T00:07:02Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 66
}
```

## [2026-08-26T17:42:03Z] peer-reviewed-source-audit | Registered journal sources and reviewer-response evidence

```json
{
  "claims": 3,
  "priority_scheme": [
    "P0",
    "P1",
    "P2"
  ],
  "sources": 7
}
```

## [2026-08-26T17:42:03Z] compile | Regenerated interlinked wiki pages

```json
{
  "claims": 67,
  "measurements": 95,
  "papers": 25,
  "review_comments": 32,
  "review_evidence_suggestions": 40,
  "topics": 23
}
```

## [2026-08-26T17:42:04Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 67
}
```

## [2026-08-30T11:11:16Z] compile | Applied complete Karpathy-style workflow to the local corpus

```json
{
  "compiled": {
    "claims": 70,
    "measurements": 95,
    "papers": 26,
    "review_comments": 32,
    "review_evidence_suggestions": 40,
    "topics": 23
  },
  "lint": {
    "broken_links": [],
    "orphan_pages": [],
    "pages": 68
  },
  "proposed_claims": 67,
  "proposed_measurements": 95,
  "review_comments": 32,
  "review_evidence_suggestions": 40,
  "topics": {
    "assignments": 155,
    "documents": 26,
    "topics": 23
  }
}
```

## [2026-08-30T11:13:32Z] baseline-evidence | Registered graph-derived Luta et al. (2021) manuscript baseline measurement for review

```json
{
  "document_doi": "10.3390/agronomy11081448",
  "measurement_id": "measurement_luta2021_openfield_fig7_range",
  "verification_status": "proposed"
}
```

## [2026-08-30T11:13:32Z] compile | Regenerated interlinked wiki pages

```json
{
  "claims": 70,
  "measurements": 96,
  "papers": 26,
  "review_comments": 32,
  "review_evidence_suggestions": 40,
  "topics": 23
}
```

## [2026-08-30T11:13:32Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 68
}
```

## [2026-08-30T11:17:43Z] baseline-evidence | Registered graph-derived Luta et al. (2021) manuscript baseline measurement

```json
{
  "document_doi": "10.3390/agronomy11081448",
  "measurement_id": "measurement_luta2021_openfield_fig7_range",
  "verification_status": "verified"
}
```

## [2026-08-30T11:17:44Z] compile | Regenerated interlinked wiki pages

```json
{
  "claims": 70,
  "measurements": 96,
  "papers": 26,
  "review_comments": 32,
  "review_evidence_suggestions": 40,
  "topics": 23
}
```

## [2026-08-30T11:17:44Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 68
}
```

## [2026-08-30T16:01:43Z] compile | Regenerated interlinked wiki pages

```json
{
  "claims": 70,
  "measurements": 96,
  "papers": 26,
  "review_comments": 32,
  "review_evidence_suggestions": 40,
  "topics": 23
}
```

## [2026-08-30T16:01:47Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 68
}
```

## [2026-08-30T16:22:15Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 69
}
```

## [2026-08-31T00:10:12Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 69
}
```

## [2026-08-31T02:07:23Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 69
}
```

## [2026-08-31T04:58:09Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 69
}
```

## [2026-08-31T23:27:20Z] stage-monthly-value-review | Imported completed monthly value decisions into provenance-backed wiki staging

```json
{
  "counts": {
    "blockers": {
      "category_crosswalk": 31,
      "tier_confirmation": 44,
      "unit_or_activity_basis": 14
    },
    "decisions": {
      "Approve for wiki + TIDBRepo staging": 55,
      "Wiki context only": 11
    },
    "staging": {
      "payload_preview_ready": 3,
      "staged_with_blockers": 52,
      "wiki_context": 11
    },
    "total": 66
  },
  "created_at": "2026-08-31T23:26:14.553Z",
  "database_write_performed": false,
  "run_id": "2026-08-30-final",
  "source_workbook": "outputs/01a0507e-5e8e-7dc2-be97-52906a1658b5/monthly_value_extraction_review_2026-08-30.xlsx",
  "source_workbook_sha256": "01d7c8d67102b534247b53b7d3c22e94c2deb1a4035012c9af7bc09178a9288e",
  "tidbrepo_snapshot": "analysis_ch4_emission_factor_malaysia/data/raw/tidbrepo_methane_emission_factor_2026-08-28.json",
  "tidbrepo_snapshot_sha256": "f75a22d2a07e2fae777bd9a639c2b91ab21d6b07e0d1bfd2b46a46a27286c830",
  "unit_policy": "knowledge_base/config/tidbrepo_unit_policy.json",
  "upload_performed": false
}
```

## [2026-08-31T23:27:20Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 70
}
```

## [2026-09-20T08:20:29Z] curate-paper | Added the reviewed Shah Alam landfill paper and six blocked values to the wiki

```json
{
  "candidate_id": "candidate_216934de1a1ef46a",
  "doi": "10.46754/jssm.2025.11.004",
  "review_ids": [
    "MV-014",
    "MV-015",
    "MV-016",
    "MV-017",
    "MV-018",
    "MV-019"
  ],
  "tidbrepo_write": false
}
```

## [2026-09-20T08:20:33Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 71
}
```

## [2026-09-20T08:27:17Z] curate-paper | Added four monthly-candidate paper pages for all remaining context-only values

```json
{
  "candidate_ids": [
    "candidate_7e8229dafd3351d1",
    "candidate_d3b4b8d8fc03840a",
    "candidate_a77001951c8051cf",
    "candidate_3a6645d40d73eb29"
  ],
  "review_ids": [
    "MV-002",
    "MV-011A",
    "MV-011B",
    "MV-011C",
    "MV-011D",
    "MV-011E",
    "MV-025",
    "MV-026",
    "MV-027",
    "MV-028",
    "MV-029"
  ],
  "tidbrepo_write": false,
  "sqlite_scientific_write": false
}
```

## [2026-09-20T08:29:09Z] lint | Checked wiki links and orphan pages

```json
{
  "broken_links": [],
  "orphan_pages": [],
  "pages": 75
}
```
## 2026-10-28 | October monthly workflow audit

Inspected run `20260930T195143Z` without regenerating its original files. Diagnosed the candidate's extraction skip (score 6, required 8), corrected future review status/count reporting, and added regression tests. Verified the UiTM full text separately and recorded a context-only screening recommendation with source checksum and page locators in [[findings/october-2026-workflow-audit|October workflow audit]]. Added proposed LLM screening, source verification, backlog, and review-preservation improvements. Complete new run packages remain local; tracked history is preserved. No scientific database write, TIDBRepo upload, timer change, or merge.

## 2026-10-28 | Monthly notifications and unverified queue synchronization

Added durable run summaries and a Gmail outbox, an explicitly unverified literature queue, provenance-preserving curated metadata, and validation/test gates before development-branch publication. Seeded [[unverified-literature/20260930T195143Z|October's unverified queue]] from the existing run without regenerating its evidence. Scientific promotion remains a separate human-reviewed change. The selected notification destination is configured through the connected Gmail delivery bridge. No scientific database write, TIDBRepo upload, or timer/service schedule modification.

## 2026-10-28 | Owner excluded the October HCC candidate

Recorded the owner's explicit exclusion in [[findings/literature-review-hcc-2026-10-28|the paper review decision]] and a separate provenance-linked JSON review record. Closed the October paper queue without rewriting original discovery metadata or local processing evidence. Queue regeneration now retains completed owner decisions. No measurement verification, TIDBRepo write, or timer change.

## 2026-10-28 | Owner approved August's 32 saved screening suggestions

Recorded A01–A04 as context-only and A05–A32 as excluded, following the owner's explicit approval of the numbered list. Preserved the original August screening gate and its earlier decisions; linked 32 separate owner-review records to its checksum. August now has zero pending paper-screening decisions. The 66 completed value decisions and six landfill conversion blockers are unchanged. September's two paper reviews and three measurement proposals remain pending. See [[findings/august-2026-remaining-screening-review|the approved August list]]. No new measurement verification, TIDBRepo upload, or timer change.

## 2026-10-28 | Owner completed September screening and requested extraction

Recorded S01 as excluded and S02 as retained for extraction. Created a new local source-review attempt for S03–S05, retaining the original September package unchanged. Inspected PDF text and rendered tables; preserved conflicting S03/S04 figures and corrected S05 to the full 56–66 mL batch range with six source conditions. All three measurements remain unverified proposals; no preferred conflicting value or inventory conversion is imposed. See [[findings/september-2026-screening-and-extraction-review|the extraction and scientific review queue]]. No scientific database write, TIDBRepo upload, or timer change.

## 2026-10-28 | Owner approved R01–R04 suitability dispositions

Recorded the owner’s approval of R01/R02 wiki-only with database use on hold, R03 as a factor candidate pending full-text verification, and R04 as wiki-only with unresolved source conflicts retained. Linked separate decision records to preserved evidence, updated paper annotations and monthly queues, and retained all original measurement verification statuses. No TIDBRepo write, timer change or merge. See [[findings/original-corpus-tidbrepo-reconciliation-2026-10-28|the reconciliation and suitability decisions]].

## 2026-10-29 | Owner authorized R03 upload; submission prepared

Cross-checked R03 Table 3 mean/SD, outlier exclusion, Maludam site and soil-chamber conditions against stored full text and author-posted full text, with publisher abstract corroboration. Prepared one explicitly conditioned peat-land row using the existing unit policy; no duplicate DOI or corresponding mean in 180 live rows. Submission remains pending authenticated access; no TIDBRepo write confirmed. Original scientific records, raw evidence, timer and other paper decisions are unchanged. See [[papers/2019-carbon-dioxide-and-methane-emissions-from-peat-soil-in-an-undrained-tropical-pea-a6bc32|R03 provenance]].

## 2026-10-29 | Direct API path for the authorized R03 submission

Browser SSO returned to an unauthenticated UI. Added a manual HTTPS Basic-authentication helper with hidden, unsaved password input, owner-authorization and source-condition checks, complete duplicate checking, a locked local submission receipt, no blind retries, the documented data wrapper, and read-back verification. It is separate from scheduled discovery and does not alter the timer. Submission still awaits the owner’s local credential input.

## 2026-10-29 | R03 uploaded through the API and independently verified

The owner ran the manual API helper with a hidden local credential prompt. HTTP 201 and the local verified receipt identify row 181. Independently read all 181 public rows: one R03 DOI record with mean 0.158, SD 0.144 kg CH4 ha^-1 day^-1 and the full source-specific condition; all previous 180 rows are unchanged. Updated curated authorization/provenance and wiki status. No credential is stored or committed. Original SQLite verification flags, R01/R02/R04 dispositions, timer and main branch remain unchanged.

## 2026-10-29 | Owner closed Q01 and Q02 existing-entry checks

Recorded Q01 as closed with the approximately 0.25% sago conversion difference accepted as negligible, and Q02 as closed on owner confirmation that the paddy issue was resolved previously. Retained original comparisons and separate provenance-linked closure records. Updated the current queue so neither item is presented as pending. No database value, scientific verification flag, timer or schedule change. See [[findings/original-corpus-tidbrepo-reconciliation-2026-10-28|the reconciliation and closure history]].

## 2026-10-29 | Guided R01/R02 factor assessment prepared

Reconstructed R01 Table 2 processing alternatives from stored full-page text, identifying the authors’ preferred 9.8–10.8 annual range. Retrieved and visually checked R02 accepted-manuscript results/caption, separating signed seasonal uptake from approximate primary-forest emission and preserving SE/sample-size limitations. Both source DOIs are absent from 181 current live rows. Saved source-specific assessment/provenance and guided wiki choices; no owner decision, scientific-status change or upload is inferred.

## 2026-10-29 | Owner staged R01 range and retained R02 wiki-only

Recorded the explicit owner decisions separately from the assessment. Staged one R01 author-preferred annual method-estimate range with full source provenance, original and normalized bounds, empty mean/median/SD, and incomplete visual/source/upload gates. R02 remains wiki-only with no further database action requested. Original evidence and scientific verification flags are preserved. No TIDBRepo write, timer change or merge.

## 2026-10-29 | Restored focus to new automated discoveries

The owner clarified that old original-corpus papers should not be presented as the new monthly literature backlog. R01/R02 assessments remain preserved as legacy history; R01 further visual checking is deferred outside the active monthly queue. Confirmed zero pending August–October paper-screening decisions and that discovery already excludes known identities by default. Read the next timer trigger as 1 November 2026 at 03:48:11 WITA; no timer or schedule change.
