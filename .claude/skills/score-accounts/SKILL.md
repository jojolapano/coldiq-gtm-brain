---
name: score-accounts
description: >
  Step 2 of the GTM Brain workflow. Enrich the companies from 01_signals with firmographics and
  score them with the rubric in CLAUDE.md §4 using scripts/score.py, producing
  data/<campaign>/02_scored_<YYYYMMDD>.csv with tiers. Use when the user says "run step 2",
  "score accounts" or "tier the list". Delegates the enrichment playbook to coldiq:tam-scoring.
---

# score-accounts

## Rubric
CLAUDE.md §4 is the only rubric. coldiq:tam-scoring uses other thresholds (65/50/35):
ignore them (rule 8). The math lives in `scripts/score.py` so the same input always gives
the same score. Never score in your head.

## Procedure
1. Read the latest `01_signals_*.csv` for the campaign named in CLAUDE.md §0.
2. Drop obvious DQs BEFORE paying for enrichment (coldiq:tam-scoring principle):
   rows without a domain, excluded customers, data/enrichment providers.
3. Load `coldiq:tam-scoring` and use the company-enrichment source it lists to get, per domain:
   employees, industry, HQ country, last funding date, known tools.
   Map it to a ColdIQ MCP tool first. Cost gate (rule 5): 5 rows first, report credits, wait for "go".
4. Fill the enrichment columns below. Unknown stays empty (rule 2): the script gives 0 points
   and adds a flag.
5. Run: `python3 scripts/score.py <input_enriched.csv> <output_scored.csv>`
6. Print: count per tier, top 5 accounts with their breakdown, every flag.

## Enrichment columns (added to the 01 columns)
| Column | Values |
|---|---|
| employees | integer |
| is_b2b_saas_ai | yes / no / empty |
| hq_country | ISO-2 (FR, ES, DE…) |
| has_outbound_motion | yes / no / empty (SDR/BDR team or sequencing tool seen) |
| funding_date | YYYY-MM-DD of last round, empty if none found |
| data_tools_count | integer (data/enrichment tools detected) |
| is_data_provider | yes / no |

## Output — `data/<campaign>/02_scored_<YYYYMMDD>.csv`
All input columns + `fit_score`, `signal_score`, `total`, `tier`, `breakdown`, `flags`.
