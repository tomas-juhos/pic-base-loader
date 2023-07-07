"""Init for file loader Queries."""

from .astec import Queries as AstecQueries
from .cleanup import Queries as CleanupQueries
from .market_cap import Queries as MarketCapQueries
from .returns import Queries as ReturnsQueries
from .shares_out import Queries as SharesOutQueries
from .volume import Queries as VolumeQueries

__all__ = ["AstecQueries", "CleanupQueries", "MarketCapQueries", "ReturnsQueries", "SharesOutQueries"]
