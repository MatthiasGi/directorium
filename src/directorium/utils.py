from datetime import date, datetime


def normalize_date(date: date | datetime) -> date:
    return date.date() if isinstance(date, datetime) else date

def easter(year: int | date | datetime) -> date:
    if isinstance(year, datetime) or isinstance(year, date):
        year = year.year
    a, b, c = year % 19, year // 100, year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    return date(year, f // 31, f % 31 + 1)
