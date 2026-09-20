# Malaysian methane literature-update review

> Nothing in this package has been uploaded to TIDBRepo.

For each row in `review.csv`, verify the PDF page and evidence quote, then set `decision` to `approve`, `reject`, or `needs_changes`. Approved rows must have sector, category, condition, tier, statistic field, target unit, URL, and DOI completed.

## Provenance chain

OpenAlex discovery record → open-access source URL → SHA-256-frozen PDF → page-numbered evidence quote → exact printed value/unit → reviewer decision → upload payload.

Candidate papers awaiting screening: **2**
Proposals awaiting review: **3**
Papers requiring manual full-text retrieval or a retrieval retry: **1**
