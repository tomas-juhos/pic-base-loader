"""Market cap queries."""
from .base import BaseQueries


class Queries(BaseQueries):
    """Market cap queries class."""

    UPSERT = (
        "INSERT INTO daily_base ("
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
        "           rtn"
        ") VALUES %s "
        "ON CONFLICT (datadate, gvkey) DO "
        "UPDATE SET "
        "           datadate=EXCLUDED.datadate, "
        "           gvkey=EXCLUDED.gvkey, "
        "           market_cap=EXCLUDED.market_cap; "
    )
