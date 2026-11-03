"""
RGAR proposal email — date helper.

Never hand-compute the day-of-week or the shortfall period. Always run this
script and use its output directly in the template.

Usage:
    python3 rgar_dates.py

Then call the functions below from a short inline script, or import them.
"""
from datetime import date
import calendar


def format_date_with_day(d: date) -> str:
    """e.g. date(2026, 7, 2) -> 'Thursday, 02/07/2026'"""
    return f"{calendar.day_name[d.weekday()]}, {d.strftime('%d/%m/%Y')}"


def format_meeting_dates_list(dates: list[date]) -> str:
    """
    Formats a list of meeting dates as they appear in the opening line, e.g.:
    one date   -> "Thursday, 02/07/2026"
    two dates  -> "Thursday, 19/02/2022 & Tuesday, 24/02/2026"
    3+ dates   -> "Thursday, 19/02/2022, Tuesday, 24/02/2026 & Thursday, 02/04/2026"
    """
    formatted = [format_date_with_day(d) for d in dates]
    if len(formatted) == 1:
        return formatted[0]
    return ", ".join(formatted[:-1]) + " & " + formatted[-1]


def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def format_shortfall_date(d: date) -> str:
    """e.g. date(2026, 8, 1) -> '1st August 2026' (no day-of-week — only meeting dates get those)"""
    return f"{ordinal(d.day)} {calendar.month_name[d.month]} {d.year}"


def shortfall_period(next_meeting_date: date, years_until_retirement: int) -> tuple[str, str]:
    """
    Start = 1st of the month FOLLOWING the next Teams meeting date.
    End   = Start + years_until_retirement (from the RGAR's "Years until
            retirement" figure), same month/day.

    Returns (start_str, end_str) already formatted e.g. ('1st August 2026', '1st August 2044').
    """
    if next_meeting_date.month == 12:
        start = date(next_meeting_date.year + 1, 1, 1)
    else:
        start = date(next_meeting_date.year, next_meeting_date.month + 1, 1)

    end = date(start.year + years_until_retirement, start.month, 1)

    return format_shortfall_date(start), format_shortfall_date(end)


if __name__ == "__main__":
    # Self-check against the worked example from the training conversation:
    # Next meeting: Thursday 02/07/2026, Years until retirement: 18
    # Expected: start = 1st August 2026, end = 1st August 2044
    start, end = shortfall_period(date(2026, 7, 2), 18)
    assert start == "1st August 2026", start
    assert end == "1st August 2044", end

    assert format_date_with_day(date(2026, 7, 2)) == "Thursday, 02/07/2026"

    # Note: an earlier hand-typed version of this email said "Thursday, 19/02/2022",
    # but 19/02/2022 was actually a Saturday — exactly the kind of manual date error
    # this script exists to prevent. Always trust the computed day, not a typed one.
    dates = [date(2022, 2, 19), date(2026, 2, 24), date(2026, 4, 2)]
    assert format_meeting_dates_list(dates) == (
        "Saturday, 19/02/2022, Tuesday, 24/02/2026 & Thursday, 02/04/2026"
    )

    print("All self-checks passed.")
    print("Example shortfall period:", start, "->", end)
