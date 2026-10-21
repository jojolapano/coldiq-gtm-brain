"""Deterministic account scorer for the GTM Brain (rubric: CLAUDE.md §4).

Usage:
    python3 scripts/score.py <input_enriched.csv> <output_scored.csv> [--today YYYY-MM-DD]

Same input + same --today = same output. Unknown values score 0 and add a flag (rule 2).
"""
import csv
import sys
from datetime import date

EU = {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT",
      "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"}
SCORE_COLUMNS = ["fit_score", "signal_score", "total", "tier", "breakdown"]
# Known ColdIQ customers (brain/offer.md exclusion list), matched on lowercase company name.
EXCLUDED = {"novel", "hemlane", "airops", "puzzle", "teikametrics"}


def parse_date(value):
    try:
        return date.fromisoformat(value.strip())
    except (AttributeError, ValueError):
        return None


def parse_int(value):
    try:
        return int(str(value).strip())
    except ValueError:
        return None


def tier_for(total):
    if total >= 75:
        return "Tier 1"
    if total >= 60:
        return "Tier 2"
    if total >= 45:
        return "Tier 3"
    return "DQ"


def score_row(row, today):
    breakdown, flags = [], [f for f in row.get("flags", "").split(";") if f]
    yes = lambda key: row.get(key, "").strip().lower() == "yes"
    unknown = lambda key: row.get(key, "").strip() == ""

    employees = parse_int(row.get("employees", ""))

    # Disqualifiers
    if row.get("company_name", "").strip().lower() in EXCLUDED:
        return 0, 0, "DQ", ["DQ: existing ColdIQ customer"], flags
    if yes("is_data_provider"):
        return 0, 0, "DQ", ["DQ: data/enrichment provider"], flags
    if employees is not None and employees < 10:
        return 0, 0, "DQ", [f"DQ: {employees} employees (< 10)"], flags

    # Fit score /50
    fit = 0
    if yes("is_b2b_saas_ai"):
        fit += 15; breakdown.append("B2B SaaS/AI +15")
    elif unknown("is_b2b_saas_ai"):
        flags.append("unknown is_b2b_saas_ai")
    if employees is None:
        flags.append("unknown employees")
    elif 20 <= employees <= 500:
        fit += 15; breakdown.append(f"{employees} employees +15")
    hq = row.get("hq_country", "").strip().upper()
    if hq in {"FR", "ES"}:
        fit += 10; breakdown.append(f"HQ {hq} +10")
    elif hq in EU:
        fit += 5; breakdown.append(f"HQ {hq} (EU) +5")
    elif not hq:
        flags.append("unknown hq_country")
    if yes("has_outbound_motion"):
        fit += 10; breakdown.append("outbound motion +10")
    elif unknown("has_outbound_motion"):
        flags.append("unknown has_outbound_motion")

    # Signal score /50
    signal = 0
    posted = parse_date(row.get("posted_date", ""))
    if posted is None:
        flags.append("unknown posted_date")
    else:
        age = (today - posted).days
        if age < 30:
            signal += 30; breakdown.append(f"role posted {age}d ago +30")
        elif age <= 60:
            signal += 15; breakdown.append(f"role posted {age}d ago +15")
    funded = parse_date(row.get("funding_date", ""))
    if funded is not None and (today - funded).days <= 183:
        signal += 10; breakdown.append("funding < 6 months +10")
    tools = parse_int(row.get("data_tools_count", ""))
    if tools is not None and tools >= 2:
        signal += 10; breakdown.append(f"{tools} data tools +10")

    tier = tier_for(fit + signal)
    if row.get("is_b2b_saas_ai", "").strip().lower() == "no" and tier in {"Tier 1", "Tier 2"}:
        tier = "Tier 3"; breakdown.append("not B2B SaaS/AI: capped at Tier 3")
    return fit, signal, tier, breakdown, flags


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    today = date.today()
    if "--today" in argv:
        today = date.fromisoformat(argv[argv.index("--today") + 1])
    with open(argv[1], newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows, fields = list(reader), list(reader.fieldnames)
    if "flags" not in fields:
        fields.append("flags")
    out_fields = fields + [c for c in SCORE_COLUMNS if c not in fields]
    scored = []
    for row in rows:
        fit, signal, tier, breakdown, flags = score_row(row, today)
        row.update(fit_score=fit, signal_score=signal, total=fit + signal, tier=tier,
                   breakdown=" | ".join(breakdown), flags=";".join(flags))
        scored.append(row)
    scored.sort(key=lambda r: r["total"], reverse=True)
    with open(argv[2], "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(scored)
    counts = {}
    for r in scored:
        counts[r["tier"]] = counts.get(r["tier"], 0) + 1
    print(f"Scored {len(scored)} accounts:", ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main(sys.argv)
