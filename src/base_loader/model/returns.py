"""Returns model."""

from datetime import datetime
from decimal import Decimal
from typing import Optional, Tuple

from .base import Modeling


class Returns(Modeling):
    """Returns record object class."""

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
    def build_record(cls, record: Tuple) -> "Returns":
        """Builds Returns record object.

        Args:
            record: record from returns_v2 file.

        Returns:
            MarketCap record object.
        """
        res = cls()

        res.datadate = datetime.strptime(record[1], "%Y-%m-%d")
        res.gvkey = int(record[0])
        res.rtn = (
            Decimal(record[2])
            if record[2] and not Decimal(record[2]).is_nan() and record[2] != "NaN"
            else None
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
