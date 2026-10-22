---
name: write-copy
description: >
  Step 5 of the GTM Brain workflow. Write a 2-email sequence for each verified contact in
  04_enriched, in the "3 campaign ideas" format, and write data/<campaign>/05_copy_<YYYYMMDD>.csv.
  Use when the user says "run step 5", "write copy" or "write the emails". Delegates the copy
  method to coldiq:cold-email-copy. Free step: no ColdIQ call. Does NOT send anything.
---

# write-copy

## Inputs
- Latest `04_enriched_*.csv` (contacts with a verified email only).
- `brain/offer.md`, `brain/proof.md`, `brain/voice.md`, CLAUDE.md §8.
- The step 1 signal for each account (role title, posted date, signal_url).

## Procedure
1. Load `coldiq:cold-email-copy`. Produce its STRATEGY BRIEF once for the campaign and show it
   before writing. Our rules win where they differ (rule 8): CLAUDE.md §8 and brain/voice.md.
2. Closed claim set: only facts from brain/offer.md and brain/proof.md. Never turn a capability
   into a promised result. Never cite a customer result as an API result (see brain/proof.md note).
3. Per-person anchor = the open role (title + how long it has been open). If an account has no
   usable anchor, write nothing for it and flag it.
4. For each contact write:
   - `email_1`: opener on the signal (fact, no flattery) + 3 bullets = 3 campaign ideas their new
     GTM engineer could run on ColdIQ in week 1, specific to their market + one soft question.
     No meeting ask, no link. 75–90 words, every sentence under 20 words.
   - `email_1_b` (Tier 1 only): same anchor, different first bullet, for A/B testing.
   - `email_2`: short follow-up (40–60 words), one new idea, same soft question style.
   - `subject`: 3–5 words, lowercase, no clickbait.
5. Language = contact country (FR → French, "vous"; ES → Spanish, "tú"; else English).
6. Run `python3 scripts/validate_copy.py <05_copy.csv>`. Fix every error, re-run until it passes.
7. Print: emails written, accounts skipped (with reason), validator result. Show 2 examples.

## Output — `data/<campaign>/05_copy_<YYYYMMDD>.csv`
Columns: `domain`, `company_name`, `tier`, `first_name`, `last_name`, `email`, `language`,
`subject`, `email_1`, `email_1_b`, `email_2`, `anchor`, `flags`.

## Never
- Send, schedule or load anything (rule 9). This step writes a file only.
- Invent a fact about the prospect, a number, or a customer result.
- Write people's names anywhere outside data/.
