---
name: detect-signals
description: >
  Step 1 of the GTM Brain workflow. Find companies with an open GTM Engineer / Growth Engineer /
  RevOps role in France and Spain and write them to data/<campaign>/01_signals_<YYYYMMDD>.csv.
  Use when the user says "run step 1", "detect signals" or "find companies hiring GTM engineers".
  Delegates the sourcing playbook to coldiq:signal-detection. Does NOT score accounts (step 2).
---

# detect-signals

## Inputs
- `CLAUDE.md` (rules, campaign name in §0) and `brain/icp.md`.
- From the user: country (FR, ES or both) and max rows (default 5 for a test).

## Procedure
1. Read `brain/icp.md` and the exclusion list in `brain/offer.md`.
2. Load `coldiq:signal-detection` for the playbook. The signal used here is hiring:
   prefer the cheapest job-openings source it lists before the 2–3 credit sources.
3. Map each endpoint you plan to use to an available ColdIQ MCP tool and show the mapping.
   If no MCP tool matches, stop and say so. Do not call the REST API by hand.
4. Search job postings with these titles (any language): "GTM Engineer",
   "Go-to-Market Engineer", "Growth Engineer", "RevOps", "Revenue Operations",
   "Ingénieur GTM", "Ingeniero GTM". Locations: France, Spain. Posted within the last 60 days
   (hiring freshness window in coldiq:signal-detection).
5. Cost gate (CLAUDE.md rule 5): run on 5 rows first, report the credits the platform shows,
   wait for "go" before any larger run.
6. Drop excluded companies (brain/offer.md) and duplicates (same domain = same company).
7. Write the CSV, then print: rows kept, rows dropped (with reason), credits used.

## Output contract — `data/<campaign>/01_signals_<YYYYMMDD>.csv`
| Column | Rule |
|---|---|
| company_name | as published |
| domain | lowercase, no `www.`; empty if unknown + flag |
| country | FR / ES / other (country of the posting) |
| role_title | exact title of the posting |
| posted_date | YYYY-MM-DD; empty if unknown + flag |
| signal_url | link to the posting (mandatory, rule 3) |
| source_tool | MCP tool used |
| detected_at | today, YYYY-MM-DD |
| flags | semicolon-separated issues, empty if none |

## Never
- Invent a posting date, a domain or a URL (rule 2).
- Enrich companies here: it costs credits and belongs to step 2.
