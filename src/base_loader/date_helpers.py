"""Date helpers."""

from datetime import datetime, timedelta


def one_day_forward(d: datetime) -> datetime:
    if d.weekday() == 4:
        return d + timedelta(days=3)
    else:
        return d + timedelta(days=1)


def one_day_backwards(d: datetime) -> datetime:
    if d.weekday() == 0:
        return d - timedelta(days=3)
    else:
        return d - timedelta(days=1)
