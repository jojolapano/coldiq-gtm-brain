"""Tests for scripts/validate_copy.py — fictitious copy only. Run: python3 scripts/test_validate_copy.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_copy import check_row, words  # noqa: E402

EMAIL_1 = """Saw you opened a GTM Engineer role three weeks ago. Here are three plays they could ship in week one:
- Score every account that visits your pricing page against your current ICP and alert sales within the hour.
- Detect companies hiring SDRs in France and route them to a dedicated sequence the same day.
- Enrich your inbound demo requests with headcount, funding date and stack before anyone books a call.
Each play runs on one API key instead of five vendor contracts. Would any of these be worth a test?"""

EMAIL_2 = """One more idea for your future GTM engineer. Track job changes of your best customers and reach out in their first month. Former users often know the product already, so the first conversation starts warmer than a cold one. Is that a motion your team already runs today?"""

BASE = {"tier": "Tier 2", "email": "test@example.test", "subject": "three plays for week one",
        "email_1": EMAIL_1, "email_1_b": "", "email_2": EMAIL_2, "company_name": "Test Co"}


def test_valid_row_passes():
    assert words(EMAIL_1) <= 90, words(EMAIL_1)
    assert check_row(dict(BASE)) == [], check_row(dict(BASE))


def test_meeting_ask_fails():
    row = dict(BASE, email_1=EMAIL_1.replace("worth a test?", "worth a demo?"))
    assert any("meeting ask" in e for e in check_row(row))


def test_link_fails():
    row = dict(BASE, email_2=EMAIL_2 + " See https://example.test")
    assert any("link" in e for e in check_row(row))


def test_two_bullets_fail():
    lines = EMAIL_1.splitlines()
    row = dict(BASE, email_1="\n".join(lines[:2] + lines[3:]))
    assert any("bullets" in e for e in check_row(row))


def test_tier1_needs_variant_b():
    row = dict(BASE, tier="Tier 1")
    assert any(e.startswith("email_1_b") for e in check_row(row))


def test_long_subject_fails():
    row = dict(BASE, subject="three amazing plays your new hire could run")
    assert any("subject" in e for e in check_row(row))


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for t in tests:
        t()
    print(f"{len(tests)} tests passed")
