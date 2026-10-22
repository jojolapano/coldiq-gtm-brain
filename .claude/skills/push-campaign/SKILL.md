---
name: push-campaign
description: >
  Step 6 of the GTM Brain workflow. Turn 05_copy into an import-ready CSV for a sequencer
  (one row per contact per step) at data/<campaign>/06_campaign_export_<YYYYMMDD>.csv.
  Use when the user says "run step 6", "export the campaign" or "prepare the import".
  Export only: never calls a sequencer, sending, mailbox or ad endpoint (rule 9).
---

# push-campaign

## Procedure
1. Read the latest `05_copy_*.csv`. Stop if `scripts/validate_copy.py` does not pass on it.
2. Keep contacts with a verified email only. Drop and list any other row.
3. Write one row per contact per step:
   - step 1 = `email_1` (Tier 1: variant A and B split 50/50, alternating rows, column `variant`),
   - step 2 = `email_2`, `delay_days` = 3.
4. Print: contacts exported, rows written, A/B split, rows dropped (with reason).
5. Remind the user that a human imports and launches the file (rule 4).

## Output — `data/<campaign>/06_campaign_export_<YYYYMMDD>.csv`
Columns: `email`, `first_name`, `last_name`, `company_name`, `language`, `step`, `delay_days`,
`variant`, `subject`, `body`.

## Never
- Call `coldiq:instantly-api`, `coldiq:emailbison`, `coldiq:campaign-delivery`,
  `coldiq:email-infra`, `coldiq:ad-audiences` or any endpoint that sends, uploads or buys.
- Write people's names anywhere outside data/.
