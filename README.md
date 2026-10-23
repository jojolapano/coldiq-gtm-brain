# ColdIQ GTM Brain

Outbound for ColdIQ's Unified API, built **on** ColdIQ: Claude Code + the ColdIQ MCP + the
`coldiq:` skills, orchestrated by a project-level GTM brain.

Target: B2B SaaS / AI companies in France and Spain that are **hiring a GTM engineer right now**.
They are about to build a data + enrichment stack; ColdIQ is that stack on day one.

> **Demo run, not sent.** The campaign was built end to end on live data, but no email was sent:
> sending outreach on ColdIQ's behalf is ColdIQ's call. `data/` (names, emails) is git-ignored.

---

## Results — first live run (2026-10-21 → 22)

| Step | Output |
|---|---|
| 1. Detect signals | 10 job postings bought → 5 accounts kept (+3 saved for later, not re-bought) |
| 2. Score accounts | 5 scored: 1 Tier 1, 1 Tier 2, 3 Tier 3 |
| 3. Find buyers | 4 contacts on the 2 Tier 1–2 accounts (founders + 1 Head of Sales) |
| 4. Enrich | 4 / 4 emails valid, all on the account domain |
| 5. Write copy | 4 two-email sequences, A/B on Tier 1, validator 4 / 4 |
| 6. Export | 8 import-ready rows, nothing sent |

**Cost: 30.07 credits in total** (≈ 15 credits per Tier 1–2 account reached), all on the free tier.

## How it works

```
CLAUDE.md                the map: rules, ICP rubric, buyer map, tool preferences, workflow
brain/                   ICP, offer, proof, voice — the only facts copy may use
.claude/skills/          7 skills, one per step; each delegates its playbook to a coldiq: skill
scripts/score.py         deterministic scoring (same input → same tier) + 10 tests
scripts/validate_copy.py deterministic copy QA (length, 3 ideas, no link, no meeting ask) + 6 tests
learnings.md             runs, product feedback, rubric changes
```

Design choices:
- **Orchestrate, don't duplicate.** Each step loads the matching `coldiq:` skill
  (`signal-detection`, `tam-scoring`, `apollo-search`, `contact-enrichment`, `cold-email-copy`…)
  and adds this campaign's context and rules on top.
- **Math and QA live in code, not in the prompt.** Tiers come from `score.py`; emails ship only
  when `validate_copy.py` passes.
- **Guardrails:** live price shown and approved before every paid call; no skill may send, upload
  or buy (`instantly-api`, `emailbison`, `campaign-delivery`, `email-infra`, `ad-audiences` are
  blocked); copy uses a closed claim set; people's names never leave `data/`.

## Product feedback for ColdIQ

Found while running the API for real (details and dates in `learnings.md`):

| Area | What I saw |
|---|---|
| Pricing drift in skills | `signal-detection` lists PredictLeads job openings at 0.18 cr, platform shows **2.51**. `tam-scoring` and `contact-enrichment` list Lima Data at 1 cr, platform shows **3.5**. |
| Your own data is the bargain | `find_people` (ColdIQ data first) cost **0.063 cr** for 3 people vs 9.91 cr listed for Apollo search; 3 of 4 emails came from ColdIQ data at ~0.02 cr. The skills still point to the expensive routes. |
| Billing display | `search_jobs` returned `credits_charged: 0` while 7.35 credits were taken (balance was right). |
| Cost gate | No price is shown before auto-routed `find_people` / `find_emails` calls; `search_jobs` has a 10-result minimum. |
| Data quality | The 20–500 employee filter let through an account whose record says both "11–50" and 280. Tech stacks only show website tools, never sequencers or data tools. |
| Verification | Two emails came back `valid` from a stored check dated 2026-09-20, without a fresh verify. |
| Good guard | An off-domain email was rejected and refunded, then the waterfall found the right one. |

## Next

Three rule changes are proposed in `learnings.md` (search buyers by seniority first, keep a company
description through scoring, no copy idea that depends on detecting non-website tools). Then:
scale to ~20 accounts across France and Spain within the free tier.

---

Built by Joseph Balland — enterprise BDR (Google Cloud, GetVocal), Le Wagon full-stack & AI.
