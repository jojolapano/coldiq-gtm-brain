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

### 2026-10-21 — step 3, `find_people` (campaign fr-es-gtm-hiring-v1)
- **Confirmed:** `find_people` (auto route) answered from ColdIQ's own data for a 2-domain +
  9-title search: 3 people, 0.063 credits (balance 275.15 → 275.09). Far cheaper than the
  9.91 cr/call shown for direct `/apollo/people/search`.
- **Gap:** no price is shown before an auto-routed `find_people` call (only provider endpoints list one),
  so CLAUDE.md rule 5's "confirm the price first" can't be met exactly for this tool.
- **Coverage:** no Head of Growth / RevOps / VP Sales found at either 26–34 person account; only founders.
- **2026-10-22 follow-up (AVEST):** `find_people` by domain + seniority (founder…director) instead of
  titles: 5 people, 0.104 cr (0.021/row, balance 275.09 → 274.98). Found a Head of Sales the title
  search missed ("Head of Sales" was not in the list). Searching by seniority catches title variants
  at small accounts for almost nothing.
- **Process note:** open step 2 flags accepted by the user on 2026-10-21: Reflect (no tech stack),
  AVEST (no outbound evidence, `has_outbound_motion` left unknown, stays Tier 2).
- **Process note:** open step 3 flags accepted by the user on 2026-10-22 for all 3 contacts in
  `03_contacts_20261021` (Reflect: 2, AVEST: 1): "hiring manager not identified in step 1 data"
  and "no Head of Growth/RevOps or VP Sales/CRO found". Founders kept as buyers (§5, < 50 employees).
  Also accepted on 2026-10-22: AVEST Head of Sales flag "Head of Sales mapped to rank 3 (VP Sales/CRO)".

### 2026-10-22 — step 4, `find_emails` (campaign fr-es-gtm-hiring-v1)
- **Confirmed:** `find_emails` (auto waterfall, `max_credits: 5`) found 4/4 valid emails on the account
  domain for 5.06 cr (balance 274.98 → 269.93). 3 came from ColdIQ's own data at 0.021 cr each;
  1 needed Findymail (3.57) + BounceBan verify (0.714). Charge-on-success held: misses cost 0.
- **Inconsistent verification:** 2 of the 3 own-data hits (Reflect) came back `valid` from a stored check
  dated 2026-09-20 with no fresh verify; the 3rd (AVEST) got a live BounceBan check.
  `valid` does not always mean "checked today".
- **Good guard:** ColdIQ's own data returned an off-domain email for one AVEST contact; the waterfall
  rejected it (`off_domain`), refunded it and moved to the next provider.
- **Gap:** no price is shown before an auto-routed `find_emails` call, only the per-provider list
  prices (same as `find_people`).
- **Stale doc:** `coldiq:contact-enrichment` lists `limadata.find.work_email` at 1 cr (live 3.5) and
  `findymail.verify` at 1 cr (BounceBan verify live 0.71).

### 2026-10-22 — step 5, `coldiq:cold-email-copy` (campaign fr-es-gtm-hiring-v1)
- **Conflict (rule 8):** the skill lists "lists of three" as a machine-writing tell and makes email 2
  "the platform"; CLAUDE.md §8 requires 3 bullets and one new idea in email 2. Our rules applied.

## Rubric changes

### 2026-10-21 — cap non-SaaS accounts at Tier 3 (CLAUDE.md §4)
- **Change:** `is_b2b_saas_ai = no` caps the tier at Tier 3 (not DQ). Unknown is not capped.
- **Evidence:** STATION F (startup campus, NAICS 551112/541611, `is_b2b_saas_ai = no`) scored 65 →
  Tier 2 in `02_scored_20261021`: a fresh RevOps role (+30), size, HQ and outbound points
  outweighed the missing 15 SaaS points. Without a cap it would get buyers and copy in steps 3–5.
- **Note:** decided by the user, not from send data (CLAUDE.md §9 asks for >= 50 sends per variant
  for learning-loop changes). Revisit after the first campaign results.

## Runs

### 2026-10-22 — fr-es-gtm-hiring-v1, steps 1–6 (demo run, not sent)
- **Volumes:** 10 job postings bought → 01: 5 accounts kept (+3 overflow) → 02: 5 scored
  (Tier 1: 1, Tier 2: 1, Tier 3: 3, DQ: 0) → 03: 4 contacts (Reflect 2, AVEST 2) →
  04: 4/4 valid emails → 05: 4 sequences, 2 emails each, A/B on Tier 1 → 06: 8 export rows.
- **Credits:** step 1: 7.35 | step 2: 17.50 | step 3: 0.17 | step 4: 5.06 | steps 5–7: 0 |
  total 30.07 (300 → 269.93). About 15 credits per Tier 1–2 account reached.
- **Copy:** validator 4/4. Reflect ideas rewritten for Reflect's own buyers (DRH, DAF) from a
  user-supplied description (Crunchbase, LinkedIn company page, Maddyness), because 02_enriched
  holds no company description column.
- **Reply results:** none, campaign not sent (demo).
- **Rule changes proposed (not applied, no send data yet):**
  1. find-buyers: search by domain + seniority before the title list. Evidence: the title search
     missed AVEST's Head of Sales; the seniority search found it for 0.10 cr.
  2. score-accounts: keep a `company_description` column in 02 so step 5 can write
     market-specific ideas without a manual lookup.
  3. write-copy: no idea that depends on detecting non-website tools (ATS, HRIS, sequencers)
     until a tech-stack call proves it. Evidence: step 2 stacks showed website tools only.
