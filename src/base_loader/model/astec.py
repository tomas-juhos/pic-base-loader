"""Returns model."""

from datetime import datetime
from decimal import Decimal
import logging
import numpy as np
from typing import Optional, Tuple

from base_loader.model.base import Modeling

logger = logging.getLogger(__name__)


class Astec(Modeling):
    """Short Interest Equity Curated record object class."""

    datadate: datetime
    gvkey: int

    utilization_pct: Optional[Decimal] = None
    bar: Optional[int] = None
    age: Optional[Decimal] = None
    tickets: Optional[int] = None
    units: Optional[Decimal] = None
    market_value_usd: Optional[Decimal] = None
    loan_rate_avg: Optional[Decimal] = None
    loan_rate_max: Optional[Decimal] = None
    loan_rate_min: Optional[Decimal] = None
    loan_rate_range: Optional[Decimal] = None
    loan_rate_stdev: Optional[Decimal] = None

    market_cap: Optional[Decimal] = None
    shares_out: Optional[Decimal] = None
    rtn: Optional[Decimal] = None

    @classmethod
    def build_record(cls, record) -> "Astec":
        """Builds Short Interest Equity Curated record object.

        Args:
            record: record a EquityCurated_Daily_History_XXXX.csv.

        Returns:
            Returns record object.
        """
        res = cls()

        dt64 = record[1]
        unix_epoch = np.datetime64(0, "s")
        one_second = np.timedelta64(1, "s")
        seconds_since_epoch = (dt64 - unix_epoch) / one_second

        res.datadate = datetime.utcfromtimestamp(seconds_since_epoch)
        res.gvkey = int(record[2])
        res.utilization_pct = (
            Decimal(record[3]) if record[3] and not np.isnan(record[3]) else None
        )
        res.bar = (
            int(Decimal(record[4])) if record[4] and not np.isnan(record[4]) else None
        )
        res.age = Decimal(record[8]) if record[8] and not np.isnan(record[8]) else None
        res.tickets = (
            int(Decimal(record[9])) if record[9] and not np.isnan(record[9]) else None
        )
        res.units = (
            Decimal(record[10]) if record[10] and not np.isnan(record[10]) else None
        )
        res.market_value_usd = (
            Decimal(record[11]) if record[11] and not np.isnan(record[11]) else None
        )
        res.loan_rate_avg = (
            Decimal(record[12]) if record[12] and not np.isnan(record[12]) else None
        )
        res.loan_rate_max = (
            Decimal(record[13]) if record[13] and not np.isnan(record[13]) else None
        )
        res.loan_rate_min = (
            Decimal(record[14]) if record[14] and not np.isnan(record[14]) else None
        )
        if res.loan_rate_max and res.loan_rate_min:
            res.loan_rate_range = res.loan_rate_max - res.loan_rate_min

        res.loan_rate_stdev = (
            Decimal(record[15]) if record[15] and not np.isnan(record[15]) else None
        )

        return res

    def as_tuple(self) -> Tuple:
        """Get tuple with object attributes.

        Returns:
            Tuple with object attributes.
        """
        return (
            self.datadate,
            self.gvkey,
            self.utilization_pct,
            self.bar,
            self.age,
            self.tickets,
            self.units,
            self.market_value_usd,
            self.loan_rate_avg,
            self.loan_rate_max,
            self.loan_rate_min,
            self.loan_rate_range,
            self.loan_rate_stdev,
            self.market_cap,
            self.shares_out,
            self.rtn,
        )

    @property
    def is_empty(self) -> bool:
        if (
            self.utilization_pct is None
            and self.bar is None
            and self.age is None
            and self.tickets is None
            and self.units is None
            and self.market_value_usd is None
            and self.loan_rate_avg is None
            and self.loan_rate_max is None
            and self.loan_rate_min is None
            and self.loan_rate_range is None
            and self.loan_rate_stdev is None
            and self.market_cap is None
            and self.shares_out is None
            and self.rtn is None
        ):
            return True
        else:
            return False

    @property
    def is_weekend(self) -> bool:
        if self.datadate.weekday() == 5 or self.datadate.weekday() == 6:
            return True
        else:
            return False
