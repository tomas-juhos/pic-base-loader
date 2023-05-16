"""Init for file loader Queries."""

from .astec import Queries as AstecQueries
from .market_cap import Queries as MarketCapQueries
from .returns import Queries as ReturnsQueries
from .shares_out import Queries as SharesOutQueries

__all__ = ["AstecQueries", "MarketCapQueries", "ReturnsQueries", "SharesOutQueries"]