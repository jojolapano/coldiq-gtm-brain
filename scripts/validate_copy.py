"""Deterministic QA gate for 05_copy (rules: CLAUDE.md §8, brain/voice.md, coldiq:cold-email-copy).

Usage:
    python3 scripts/validate_copy.py <05_copy.csv>
Exit code 0 = pass, 1 = errors. Same file = same result.
"""
import csv
import re
import sys

BANNED = ["i hope this finds you well", "revolutionise", "revolutionize", "game-changer",
          "game changer", "quick question", "révolutionn", "revolucion"]
MEETING_ASK = ["meeting", "15 min", "calendar", "book a call", "hop on a call", "demo",
               "rendez-vous", "réunion", "créneau", "reunión", "llamada", "agenda"]
BULLET = re.compile(r"^\s*(?:[-•*]|\d+[.)])\s+")


def words(text):
    return len(re.findall(r"\b[\w'’-]+\b", text))


def sentences(text):
    parts = []
    for line in text.splitlines():
        line = BULLET.sub("", line).strip()
        parts += [s.strip() for s in re.split(r"(?<=[.!?])\s+", line) if s.strip()]
    return parts


def check_email(label, text, lo, hi, need_bullets):
    errors = []
    if not text.strip():
        return [f"{label}: empty"]
    n = words(text)
    if not lo <= n <= hi:
        errors.append(f"{label}: {n} words (expected {lo}-{hi})")
    for s in sentences(text):
        if words(s) >= 20:
            errors.append(f"{label}: sentence of {words(s)} words: '{s[:40]}…'")
    low = text.lower()
    errors += [f"{label}: banned phrase '{b}'" for b in BANNED if b in low]
    if "http" in low or "www." in low:
        errors.append(f"{label}: contains a link")
    if need_bullets:
        bullets = sum(1 for line in text.splitlines() if BULLET.match(line))
        if bullets != 3:
            errors.append(f"{label}: {bullets} bullets (expected 3 campaign ideas)")
        # The ask is the last sentence: it must not request a meeting (CLAUDE.md §8).
        last = sentences(text)[-1].lower() if sentences(text) else ""
        errors += [f"{label}: meeting ask '{m}' in the last sentence" for m in MEETING_ASK if m in last]
    return errors


def check_row(row):
    errors = []
    n = words(row.get("subject", ""))
    if not 3 <= n <= 5:
        errors.append(f"subject: {n} words (expected 3-5)")
    errors += check_email("email_1", row.get("email_1", ""), 75, 90, True)
    if row.get("tier") == "Tier 1":
        errors += check_email("email_1_b", row.get("email_1_b", ""), 75, 90, True)
    errors += check_email("email_2", row.get("email_2", ""), 40, 60, False)
    if not row.get("email", "").strip():
        errors.append("email: missing")
    return errors


def main(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    failed = 0
    for i, row in enumerate(rows, start=2):  # line 1 = header
        errors = check_row(row)
        if errors:
            failed += 1
            print(f"Row {i} ({row.get('company_name', '?')}):")
            for e in errors:
                print(f"  - {e}")
    print(f"{len(rows) - failed}/{len(rows)} rows pass")
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
