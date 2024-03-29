"""Volume model."""

from datetime import datetime
from decimal import Decimal
import logging
from typing import Optional, Tuple

from base_loader.model.base import Modeling
from base_loader.date_helpers import one_day_forward, one_day_backwards

import numpy as np

logger = logging.getLogger(__name__)


class Volume(Modeling):
    """Volume record object class."""

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
    volume: Optional[Decimal] = None
    rtn: Optional[Decimal] = None

    @classmethod
    def build_record(cls, record) -> "Volume":
        """Volume record object.

        Args:
            record: record.

        Returns:
            Volume record object.
        """
        res = cls()

        dt64 = record[1]
        unix_epoch = np.datetime64(0, "s")
        one_second = np.timedelta64(1, "s")
        seconds_since_epoch = (dt64 - unix_epoch) / one_second

        res.datadate = datetime.utcfromtimestamp(seconds_since_epoch)
        res.gvkey = int(record[0])
        res.volume = Decimal(record[2]) if record[2] and not Decimal(record[2]).is_nan() else None

        return res

    def move_date_forward(self):
        self.datadate = one_day_forward(self.datadate)

    def move_date_backwards(self):
        self.datadate = one_day_backwards(self.datadate)

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
            self.volume,
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
            and self.volume is None
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

