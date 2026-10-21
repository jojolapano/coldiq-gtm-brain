---
name: find-buyers
description: >
  Step 3 of the GTM Brain workflow. For each Tier 1 and Tier 2 account in 02_scored, find the
  buyers (hiring manager of the open GTM role first, then Head of Growth / RevOps, VP Sales / CRO,
  Founder) and write them to data/<campaign>/03_contacts_<YYYYMMDD>.csv. Use when the user says
  "run step 3", "find buyers" or "find contacts". Delegates persona mapping to coldiq:icp-personas
  and people search to coldiq:apollo-search. Does NOT find emails or phones (step 4).
---

# find-buyers

## Inputs
- `CLAUDE.md` §5 (buyer map) and §4 tiers, `brain/icp.md` (buyer order).
- The latest `02_scored_*.csv` for the campaign named in CLAUDE.md §0.

## Procedure
1. Stop if `02_scored` has unresolved flags on Tier 1–2 rows (CLAUDE.md §7). List them.
2. Keep Tier 1 and Tier 2 rows only. Tier 3 and DQ get no contacts.
3. Load `coldiq:icp-personas` for the buying-committee method. Our buyer map (CLAUDE.md §5)
   wins over its generic roles (rule 8):
   1. Hiring manager of the open GTM role, when the posting or the company names them.
   2. Head of Growth / Head of RevOps.
   3. VP Sales / CRO.
   4. Founder / CEO, only if employees < 50.
4. Load `coldiq:apollo-search` for the people-search playbook. Map the endpoint to a ColdIQ MCP
   tool and show the mapping. If no MCP tool matches, stop and say so.
   Search by company domain + the title list above. Never search without a domain filter.
5. Cost gate (rule 5): run on 5 accounts first, report the credits the platform shows,
   wait for "go" before the rest.
6. Cap per account: Tier 1 = 3 buyers, Tier 2 = 2 buyers, taken in priority order.
7. Mark `is_hiring_manager = yes` only with evidence (named in the posting, or the title matches
   the reporting line the posting states). Otherwise `no`: a guess is not evidence.
8. Drop people whose current company domain does not match the account domain (job changers).
9. Write the CSV, then print: contacts per tier, accounts with 0 buyers found, credits used.

## Output contract — `data/<campaign>/03_contacts_<YYYYMMDD>.csv`
One row per contact.
| Column | Rule |
|---|---|
| domain | account key, joins to 02_scored |
| company_name | from 02_scored |
| tier | from 02_scored |
| signal_url | from 02_scored (rule 3) |
| first_name, last_name | as returned by the source |
| title | current title as returned |
| buyer_rank | 1–4 per the buyer map in step 3 |
| is_hiring_manager | yes / no |
| linkedin_url | empty if unknown + flag |
| country | ISO-2 of the person (drives copy language, CLAUDE.md §8); empty if unknown + flag |
| source_tool | MCP tool used |
| found_at | today, YYYY-MM-DD |
| flags | semicolon-separated issues, empty if none |

## Never
- Find or guess emails or phones here: that is step 4 (`enrich`).
- Infer a person from a name pattern or invent a title (rule 2).
- Add contacts for Tier 3 or DQ accounts.
