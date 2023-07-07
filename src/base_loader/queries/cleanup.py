"""Cleanup queries."""


class Queries:
    """Cleanup queries class."""
    # CHANGE VOLUME CONSTRAINTS BELOW IF NEEDED
    CLEAN_MKTCAP_VOL_RTN = (
        "DELETE "
        "FROM daily_base "
        "WHERE market_cap < 100 "
        "OR volume < 1000000 "
        "OR market_cap IS NULL "
        "OR volume IS NULL "
        "OR rtn IS NULL;"
    )

    CLEAN_ASTEC = (
        "DELETE "
        "FROM daily_base "
        "WHERE utilization_pct IS NULL "
        "AND bar IS NULL "
        "AND age IS NULL "
        "AND tickets IS NULL "
        "AND units IS NULL "
        "AND market_value_usd IS NULL "
        "AND loan_rate_avg IS NULL "
        "AND loan_rate_max IS NULL "
        "AND loan_rate_min IS NULL "
        "AND loan_rate_range IS NULL "
        "AND loan_rate_stdev IS NULL;"
    )

    CLEAN_GVKEYS = (
        "DELETE "
        "FROM daily_base "
        "WHERE (gvkey) IN (VALUES %s);"
    )
