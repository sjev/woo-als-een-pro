#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# ///
"""Compute the last day of a statutory term under the Algemene termijnenwet (Atw).

    tools/termijn.py 2026-11-02 4w        # Woo decision term from receipt
    tools/termijn.py 2026-11-02 4w 2w     # same, with two weeks deferral
    tools/termijn.py 2026-11-02 6w 12d    # term plus 12 days suspension

DATE is the event (receipt, notice, decision). The term starts the day after.
Chained periods: the Atw is applied per step and at the end; the later date wins.
Supported years: 2014 and later (King's Day on 27 April).
"""

from __future__ import annotations

import re
import sys
from datetime import date, timedelta

MAX_DAYS = 90  # Atw art. 4 sub a: not for terms over 90 days or twelve weeks.
MAX_WEEKS = 12


def easter(year: int) -> date:
    """Gregorian Easter Sunday (anonymous Gregorian algorithm)."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 19 * l) // 433
    month = (h + l - 7 * m + 90) // 25
    return date(year, month, (h + l - 7 * m + 33 * month + 19) % 32)


def holidays(year: int) -> set[date]:
    """Atw art. 3: algemeen erkende feestdagen, Good Friday included."""
    if year < 2014:
        raise ValueError("Years before 2014 are not supported (Koninginnedag rules differ).")
    e = easter(year)
    kings_day = date(year, 4, 27)
    if kings_day.weekday() == 6:  # Celebrated on Saturday 26 April when 27 April is a Sunday.
        kings_day = date(year, 4, 26)
    return {
        date(year, 1, 1),
        e - timedelta(days=2),  # Good Friday (art. 3 lid 2)
        e + timedelta(days=1),  # Easter Monday
        e + timedelta(days=39),  # Ascension Day
        e + timedelta(days=50),  # Whit Monday
        kings_day,
        date(year, 5, 5),
        date(year, 12, 25),
        date(year, 12, 26),
    }


def is_workday(d: date) -> bool:
    return d.weekday() < 5 and d not in holidays(d.year)


def next_workday(d: date) -> date:
    d += timedelta(days=1)
    while not is_workday(d):
        d += timedelta(days=1)
    return d


def parse_period(s: str) -> timedelta:
    m = re.fullmatch(r"(\d+)([dw])", s)
    if not m:
        raise ValueError(f"Bad period {s!r}; use e.g. 4w or 14d.")
    n = int(m.group(1))
    return timedelta(weeks=n) if m.group(2) == "w" else timedelta(days=n)


def atw_applies(periods: list[str]) -> bool:
    """Atw art. 4 sub a: a term in weeks up to twelve weeks; otherwise up to 90 days."""
    total = sum((parse_period(p) for p in periods), timedelta()).days
    in_weeks = all(p.endswith("w") for p in periods)
    return total <= (MAX_WEEKS * 7 if in_weeks else MAX_DAYS)


def last_day(event: date, period: timedelta, atw: bool = True) -> tuple[date, list[str]]:
    """Last day of a term that starts the day after `event`, with the Atw rules that applied."""
    end = event + period
    notes: list[str] = []
    if not atw:
        return end, ["Atw not applied: term longer than 90 days or twelve weeks (art. 4)."]
    if not is_workday(end):
        end = next_workday(end)
        notes.append("Extended past weekend or holiday (Atw art. 1).")
    if period.days >= 3:
        while sum(is_workday(event + timedelta(days=i)) for i in range(1, (end - event).days + 1)) < 2:
            end = next_workday(end)
            notes.append("Extended to contain two workdays (Atw art. 2).")
    return end, notes


def chain_end(event: date, periods: list[str]) -> tuple[date, list[str]]:
    """Last day of chained periods (term, deferral, suspension).

    Whether the Atw applies per step or only to the end of the chain is not settled.
    Both are computed; the later date is returned, because a premature
    ingebrekestelling has no effect.
    """
    atw = atw_applies(periods)
    total = sum((parse_period(p) for p in periods), timedelta())
    end, notes = last_day(event, total, atw)
    step = event
    for p in periods:
        step = last_day(step, parse_period(p), atw)[0]
    if step > end:
        notes.append(f"Atw per step gives {step:%Y-%m-%d}, at the end only {end:%Y-%m-%d}. The later date is given.")
    return max(end, step), notes


def report(event: date, periods: list[str]) -> str:
    """Plain-text result, shared by the CLI and the site's /termijn endpoint."""
    period = sum((parse_period(p) for p in periods), timedelta())
    end, notes = chain_end(event, periods)
    lines = [
        f"event:     {event:%Y-%m-%d %a}",
        f"term:      {period.days} days, starts {event + timedelta(days=1):%Y-%m-%d %a}",
        f"last day:  {end:%Y-%m-%d %a}",
        f"day after: {end + timedelta(days=1):%Y-%m-%d %a}",
    ]
    return "\n".join(lines + [f"note:      {note}" for note in notes]) + "\n"


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        sys.exit(__doc__)
    print(report(date.fromisoformat(argv[0]), argv[1:]), end="")


if __name__ == "__main__":
    main(sys.argv[1:])
