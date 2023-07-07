"""Astec queries."""
from .base import BaseQueries


class Queries(BaseQueries):
    """Astec queries class."""

    UPSERT = (
        "INSERT INTO {tbl} ("
        "           datadate, "
        "           gvkey, "
        "           utilization_pct, "
        "           bar, "
        "           age, "
        "           tickets, "
        "           units, "
        "           market_value_usd, "
        "           loan_rate_avg, "
        "           loan_rate_max, "
        "           loan_rate_min, "
        "           loan_rate_range, "
        "           loan_rate_stdev, "
        "           market_cap, "
        "           shares_out, "
        "           volume, "
        "           rtn"
        ") VALUES %s "
        "ON CONFLICT (datadate, gvkey) DO "
        "UPDATE SET "
        "           datadate=EXCLUDED.datadate, "
        "           gvkey=EXCLUDED.gvkey, "
        "           utilization_pct=EXCLUDED.utilization_pct, "
        "           bar=EXCLUDED.bar, "
        "           age=EXCLUDED.age, "
        "           tickets=EXCLUDED.tickets, "
        "           units=EXCLUDED.units, "
        "           market_value_usd=EXCLUDED.market_value_usd, "
        "           loan_rate_avg=EXCLUDED.loan_rate_avg, "
        "           loan_rate_max=EXCLUDED.loan_rate_max, "
        "           loan_rate_min=EXCLUDED.loan_rate_min, "
        "           loan_rate_range=EXCLUDED.loan_rate_range, "
        "           loan_rate_stdev=EXCLUDED.loan_rate_stdev; "
    )
