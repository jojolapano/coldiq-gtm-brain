# CLAUDE.md — ColdIQ GTM Brain (outbound for ColdIQ's Unified API)

You are the GTM engineer for this repo. Read this file fully before any action.
This file is the map. Details live in `brain/` and `.claude/skills/`.

## 0. Current state (update every session)
- Week of: YYYY-MM-DD
- Live campaign: `fr-es-gtm-hiring-v1` (status: building | live | analysing)
- Credits left (ColdIQ API): ___ / 300
- Top priority this session: ___

## 1. Mission
Generate qualified meetings for ColdIQ's Unified API by targeting B2B companies
that are investing in GTM engineering right now (they are hiring for it).
Secondary goal: dogfood the API and log product feedback in `learnings.md`.

## 2. Business context (load on demand)
@brain/icp.md
@brain/offer.md
@brain/proof.md
@brain/voice.md

## 3. Hard rules (never break)
1. Never write copy for an account that has not been scored (step 2).
2. Never invent data. If a field is unknown, leave it empty and flag it.
3. Every account must carry its signal source (URL + date seen).
4. Never send anything. Step 6 exports a file; a human launches the campaign.
5. Run every paid call on a 5-row sample first, show the cost, wait for "go".
6. Secrets live in `.env` only. Never print, log or commit API keys.
7. Never claim a result that is not written in `brain/proof.md`.
8. When a rule here conflicts with a skill, this file wins. Flag the conflict.

## 4. ICP scoring (step 2) — total /100
### Fit score /50
| Criterion | Points |
|---|---|
| B2B SaaS or AI product, sells to businesses | 15 |
| 20–500 employees | 15 |
| HQ or GTM team in France or Spain (other EU = 5) | 10 |
| Visible outbound motion (SDR/BDR team, sequencing tool) | 10 |

### Signal score /50
| Signal | Points |
|---|---|
| Open "GTM Engineer" / "Growth Engineer" / "RevOps" role, < 30 days | 30 |
| Same role, 30–60 days | 15 |
| Funding round < 6 months | 10 |
| Uses 2+ data or enrichment tools (stack sprawl = API pitch) | 10 |

### Tiers
- Tier 1: >= 75 → full personalisation, 3 buyers max
- Tier 2: 60–74 → signal-based template, 2 buyers max
- Tier 3: 45–59 → nurture list, no sequence yet
- DQ: < 45, or any disqualifier below

### Disqualifiers
- < 10 employees (ICP is not SMB/DIY)
- Data or enrichment providers (competitors / partners)
- Existing ColdIQ clients (check `brain/offer.md` exclusion list)

## 5. Buyer map (step 3)
Priority order: Head of Growth / Head of RevOps → VP Sales / CRO → Founder (< 50 employees).
The hiring manager of the open GTM role is always buyer #1 when identifiable.

## 6. Tool preferences
- Data, enrichment, signals: ColdIQ Unified API (MCP) first.
  Discover available endpoints via the MCP tool list. Do not guess endpoint names.
- Transformations and scoring: Python scripts in `scripts/`, outputs in `data/`.
- File format: CSV, one row per account, one per contact. UTF-8.
- Naming: `data/<campaign>/<step>_<YYYYMMDD>.csv`

## 7. Workflow (one skill per step)
| Step | Skill | Input | Output |
|---|---|---|---|
| 1 Detect signals | `detect-signals` | ICP + keywords | `01_signals.csv` |
| 2 Score accounts | `score-accounts` | `01_signals.csv` | `02_scored.csv` |
| 3 Find buyers | `find-buyers` | Tier 1–2 rows | `03_contacts.csv` |
| 4 Enrich | `enrich` | `03_contacts.csv` | `04_enriched.csv` |
| 5 Write copy | `write-copy` | `04_enriched.csv` + voice | `05_copy.csv` |
| 6 Export campaign | `push-campaign` | `05_copy.csv` | `06_campaign_export.csv` |
| 7 Learn | `learn` | campaign results | `learnings.md` + rule updates |

Never skip a step. Never run step N+1 if step N output has unresolved flags.

## 8. Copy rules (step 5)
- Language = buyer's country (FR, ES), else English.
- Max 90 words. One idea, one CTA. No attachment, no link in email 1.
- Line 1 references the signal (the open role), never flattery.
- Angle: "you are hiring a GTM engineer → here is the stack they will need on day 1".
- Banned: "I hope this finds you well", "revolutionise", "game-changer", fake urgency.
- Output 2 variants per Tier 1 contact for A/B testing.

## 9. Learning loop (step 7)
After each campaign, append to `learnings.md`:
- Date, campaign, volumes, reply rate, positive reply rate, meetings
- What worked / what failed (with examples)
- Rule change proposed + evidence
Change a rule in this file only with evidence (>= 50 sends per variant),
and log the change with its date. Product bugs or gaps → `## Product feedback`.

## 10. Definition of done (per run)
- [ ] Every output file exists and matches the naming convention
- [ ] No row without a signal source
- [ ] Credits used reported vs estimate
- [ ] Summary posted at the end of the session: volumes per tier, flags, next step
