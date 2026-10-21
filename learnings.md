# Learnings — ColdIQ GTM Brain

## Product feedback

### 2026-10-21 — step 1, `search_jobs` (campaign fr-es-gtm-hiring-v1)
- **Confirmed:** `search_jobs` pinned to `linkedin_jobs_api` works for title + France + 20–500
  employee filters. Live price 0.74 cr/job; 10 jobs cost 7.35 credits (balance 300 → 292.65).
- **Bug:** the response reported `credits_charged: 0` (top-level and in `_meta.attempts`)
  while the balance dropped by 7.35. Only `credits_remaining` / `get_credit_balance` were right.
- **Gap:** `search_jobs` has `limit` minimum 10, so a 5-row sample (CLAUDE.md rule 5) can't be
  bought exactly.
- **Stale doc:** `coldiq:signal-detection` lists `predictleads.discover.job_openings` at 0.18 cr;
  the platform shows 2.51 cr/result. It also filters by O*NET code, not job title.
- **Filter leak:** the 20–500 employee filter let through STATION F, whose LinkedIn size is
  "11-50" while its headcount is 303. Employee counts need re-checking in step 2.

### 2026-10-21 — step 2, `enrich_company` (campaign fr-es-gtm-hiring-v1)
- **Confirmed:** `enrich_company` pinned to `limadata` matched all 5 domains (`identity_match: domain`).
  Live price 3.5 cr/call; 5 calls cost 17.5 credits (balance 292.65 → 275.15).
  `credits_charged` was reported correctly here, unlike `search_jobs`.
- **Stale doc:** `coldiq:tam-scoring` lists `limadata.enrich.company` at 1 cr; the platform shows 3.5.
- **Coverage gaps:** 1 of 5 records had no tech stack (getreflect.io). Tech stacks only show website
  tools (HubSpot, WordPress…), never sequencers or data tools, so `has_outbound_motion` and
  `data_tools_count` mostly come from the job posting, not the enrichment.
- **Data conflict:** stationf.co shows headcount 280 but range "11-50 employees" in the same record.

## Rubric changes

### 2026-10-21 — cap non-SaaS accounts at Tier 3 (CLAUDE.md §4)
- **Change:** `is_b2b_saas_ai = no` caps the tier at Tier 3 (not DQ). Unknown is not capped.
- **Evidence:** STATION F (startup campus, NAICS 551112/541611, `is_b2b_saas_ai = no`) scored 65 →
  Tier 2 in `02_scored_20261021`: a fresh RevOps role (+30), size, HQ and outbound points
  outweighed the missing 15 SaaS points. Without a cap it would get buyers and copy in steps 3–5.
- **Note:** decided by the user, not from send data (CLAUDE.md §9 asks for >= 50 sends per variant
  for learning-loop changes). Revisit after the first campaign results.
