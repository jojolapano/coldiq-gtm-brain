---
name: learn
description: >
  Step 7 of the GTM Brain workflow. Log what a run taught us in learnings.md: volumes, costs,
  product feedback, and (once emails are sent) reply results, then propose rule changes with
  evidence. Use when the user says "run step 7", "log learnings" or "what did we learn".
  Free step: no ColdIQ call.
---

# learn

## Procedure
1. Read the run's files in `data/<campaign>/` and the session's notes.
2. Append to `learnings.md` under `## Runs`, one entry per run:
   date, campaign, accounts per step (01 → 06), tiers, contacts, emails written,
   credits used per step and total, credits left.
3. Product feedback (ColdIQ): add only what this run confirmed or broke, under
   `## Product feedback`, with the tool, the expected vs actual value, and the date.
4. Reply results (only once a human has sent the campaign and shared results):
   sends, replies, positive replies, meetings, per variant.
5. Rule changes: propose, never apply. A rule changes only with evidence
   (CLAUDE.md §9: >= 50 sends per variant for copy rules). A decision made by the user without
   that evidence is logged under `## Rubric changes` as a user decision.
6. Update CLAUDE.md §0 "Current state" (credits left, status, next priority). Show the diff.

## Never
- Write people's names, emails or LinkedIn URLs in learnings.md: counts and company names only.
- Change CLAUDE.md rules without the user's approval.
