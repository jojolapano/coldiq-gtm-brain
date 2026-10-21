"""Tests for scripts/score.py — fictitious companies only. Run: python3 scripts/test_score.py"""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from score import score_row

TODAY = date(2026, 10, 21)
BASE = {"is_b2b_saas_ai": "yes", "employees": "80", "hq_country": "FR",
        "has_outbound_motion": "yes", "posted_date": "2026-10-09", "funding_date": "2026-06-01",
        "data_tools_count": "1", "is_data_provider": "no", "flags": ""}


def run(**overrides):
    return score_row({**BASE, **overrides}, TODAY)


def test_tier1_paris_saas():
    fit, signal, tier, _, flags = run()
    assert (fit, signal, tier) == (50, 40, "Tier 1"), (fit, signal, tier)
    assert flags == []


def test_old_posting_drops_tier():
    fit, signal, tier, _, _ = run(posted_date="2026-08-30", funding_date="")  # 52 days
    assert (fit, signal, tier) == (50, 15, "Tier 2"), (fit, signal, tier)


def test_small_company_is_dq():
    *_, tier, breakdown, _ = run(employees="6")
    assert tier == "DQ" and "DQ" in breakdown[0]


def test_data_provider_is_dq():
    *_, tier, _, _ = run(is_data_provider="yes")
    assert tier == "DQ"


def test_unknown_values_score_zero_and_flag():
    fit, signal, tier, _, flags = run(is_b2b_saas_ai="", posted_date="")
    assert fit == 35 and signal == 10
    assert "unknown is_b2b_saas_ai" in flags and "unknown posted_date" in flags


def test_existing_customer_is_dq():
    *_, tier, breakdown, _ = run(company_name="AirOps")
    assert tier == "DQ" and "customer" in breakdown[0]


def test_other_eu_hq():
    fit, *_ = run(hq_country="DE")
    assert fit == 45


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for t in tests:
        t()
    print(f"{len(tests)} tests passed")
