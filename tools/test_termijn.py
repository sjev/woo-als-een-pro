"""Tests for termijn.py. Run: uv run --with pytest pytest tools/"""

from datetime import date, timedelta

import pytest

from termijn import atw_applies, easter, holidays, last_day, parse_period


def end(event: str, period: str) -> date:
    return last_day(date.fromisoformat(event), parse_period(period))[0]


@pytest.mark.parametrize(("year", "expected"), [(2024, date(2024, 3, 31)), (2025, date(2025, 4, 20)), (2026, date(2026, 4, 5))])
def test_easter(year: int, expected: date) -> None:
    assert easter(year) == expected


def test_holidays_2026() -> None:
    assert holidays(2026) == {
        date(2026, 1, 1), date(2026, 4, 3), date(2026, 4, 6), date(2026, 4, 27), date(2026, 5, 5),
        date(2026, 5, 14), date(2026, 5, 25), date(2026, 12, 25), date(2026, 12, 26),
    }


def test_kings_day_on_sunday_moves_to_saturday() -> None:
    assert date(2025, 4, 26) in holidays(2025)
    assert date(2025, 4, 27) not in holidays(2025)


def test_plain_term_starts_day_after_event() -> None:
    assert end("2026-11-02", "4w") == date(2026, 11, 30)


def test_weekend_extends_to_monday() -> None:
    assert end("2026-10-31", "4w") == date(2026, 11, 30)


def test_christmas_extends_past_weekend() -> None:
    assert end("2026-11-27", "4w") == date(2026, 12, 28)


def test_fifth_of_may_is_a_holiday_every_year() -> None:
    assert end("2026-04-07", "4w") == date(2026, 5, 6)


def test_two_workdays_rule() -> None:
    # 25 Dec holiday, 26-27 weekend, 28 Mon is the only workday: extend to 29 Dec.
    assert end("2026-12-24", "3d") == date(2026, 12, 29)


@pytest.mark.parametrize(("periods", "expected"), [(["12w"], True), (["13w"], False), (["85d"], True), (["90d"], True), (["91d"], False), (["12w", "6d"], True)])
def test_atw_scope(periods: list[str], expected: bool) -> None:
    assert atw_applies(periods) is expected


def test_long_term_not_extended() -> None:
    event = date(2026, 1, 3)
    result, notes = last_day(event, timedelta(weeks=13), atw=False)
    assert result == event + timedelta(weeks=13)
    assert "art. 4" in notes[0]


def test_old_year_rejected() -> None:
    with pytest.raises(ValueError):
        holidays(2013)


def test_bad_period_rejected() -> None:
    with pytest.raises(ValueError):
        parse_period("4m")
