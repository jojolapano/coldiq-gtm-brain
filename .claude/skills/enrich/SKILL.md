---
name: enrich
description: >
  Step 4 of the GTM Brain workflow. Dedupe the contacts from 03_contacts, find and verify a work
  email for each, and write data/<campaign>/04_enriched_<YYYYMMDD>.csv. Use when the user says
  "run step 4", "enrich" or "find emails". Delegates dedup to coldiq:list-dedup and the email
  waterfall to coldiq:contact-enrichment. Does NOT write copy (step 5) or send anything (rule 9).
---

# enrich

## Inputs
- The latest `03_contacts_*.csv` for the campaign named in CLAUDE.md §0.
- Earlier `04_enriched_*.csv` files for the same campaign (never pay twice for a contact).

## Procedure
1. Stop if `03_contacts` has unresolved flags (CLAUDE.md §7). List them. A flag counts as
   resolved only when the user accepted it and that is logged in `learnings.md`.
2. Load `coldiq:list-dedup`. Normalize `linkedin_url`, then dedupe on it (fallback key:
   domain + first_name + last_name). Drop contacts already present in an earlier `04_enriched`.
   Report how many rows were removed and why.
3. Load `coldiq:contact-enrichment` for the waterfall method (cheapest first, verify on hit).
   Map each step to a ColdIQ MCP tool and show the mapping. If no MCP tool matches, stop and say so.
   Input per contact: first_name, last_name, domain, linkedin_url.
4. Scope: work email only. Phones are out of scope for an email campaign unless the user asks.
5. Cost gate (rule 5): show the live price per contact the platform lists (or say it shows none),
   run on 5 contacts first, report the credits charged, wait for "go" before the rest.
6. Verification decides sendability:
   - `valid` → keep.
   - `catch_all` / `risky` → keep the email, `email_status` as returned, add flag
     `not sendable without review`.
   - `invalid` or nothing found → empty email, `email_status = not_found`, flag it.
7. If a provider returns a current company or email domain that does not match the account
   domain, drop the email and flag `possible job change`.
8. Write the CSV, then print: contacts in, deduped, valid, catch-all/risky, not found,
   credits used vs estimate. Log confirmed endpoints, prices and misses in `learnings.md`
   `## Product feedback`, and update the credit balance in CLAUDE.md §0.

## Output contract — `data/<campaign>/04_enriched_<YYYYMMDD>.csv`
One row per contact. All `03_contacts` columns, plus:
| Column | Rule |
|---|---|
| email | as returned by the provider; empty if not found or invalid |
| email_status | valid / catch_all / risky / not_found, as the verifier reports |
| email_source | MCP tool + provider that answered |
| enriched_at | today, YYYY-MM-DD |
| flags | 03 flags kept, new issues appended (semicolon-separated) |

## Never
- Guess or build an email from a name pattern (rule 2). No result means an empty email.
- Enrich contacts from Tier 3 or DQ accounts, or contacts not in `03_contacts`.
- Send, upload or load contacts into a sending tool (rule 9). Step 6 exports a file only.
- Write people's names, emails or LinkedIn URLs anywhere outside data/ (learnings.md: counts and company names only).
