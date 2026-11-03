"""
OM Tax-Free proposal email — date helper.

Never hand-compute the day-of-week for any meeting date. Always run this
script and use its output directly in the template.

Usage:
    python3 tax_free_dates.py

Then call the functions below from a short inline script, or import them.
"""
from datetime import date
import calendar


def format_date_with_day(d: date) -> str:
    """e.g. date(2026, 7, 17) -> 'Friday, 17/07/2026'"""
    return f"{calendar.day_name[d.weekday()]}, {d.strftime('%d/%m/%Y')}"


def format_meeting_dates_list(dates: list[date]) -> str:
    """
    Formats a list of meeting dates as they appear in the opening line, e.g.:
    one date   -> "Friday, 10/07/2026"
    two dates  -> "Friday, 10/07/2026 & Wednesday, 15/07/2026"
    3+ dates   -> "Friday, 10/07/2026, Wednesday, 15/07/2026 & Thursday, 16/07/2026"
    """
    formatted = [format_date_with_day(d) for d in dates]
    if len(formatted) == 1:
        return formatted[0]
    return ", ".join(formatted[:-1]) + " & " + formatted[-1]


if __name__ == "__main__":
    # Self-check on fixed dates (invented, no client).
    assert format_date_with_day(date(2026, 7, 10)) == "Friday, 10/07/2026"
    assert format_date_with_day(date(2026, 7, 17)) == "Friday, 17/07/2026"

    dates = [date(2026, 7, 10), date(2026, 7, 15)]
    assert format_meeting_dates_list(dates) == (
        "Friday, 10/07/2026 & Wednesday, 15/07/2026"
    )

    print("All self-checks passed.")
