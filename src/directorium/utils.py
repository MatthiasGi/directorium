"""
Simple utility module for reused functions that don't fit into any other module.
"""

from datetime import date, datetime


def normalize_date(date: date | datetime) -> date:
    """Returns a date object from a date or datetime object.

    Args:
        date: The date or datetime object to normalize.

    Returns:
        The normalized date object, stripped of time information.
    """
    return date.date() if isinstance(date, datetime) else date

def easter(year: int | date | datetime) -> date:
    """Calculates the date of Easter Sunday for a given year.

    If a date or datetime object is passed, the year is extracted from it.

    Args:
        year: The year for which to calculate Easter Sunday.

    Returns:
        The date of Easter Sunday for the given year.
    """
    if isinstance(year, datetime) or isinstance(year, date):
        year = year.year
    a, b, c = year % 19, year // 100, year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    return date(year, f // 31, f % 31 + 1)
