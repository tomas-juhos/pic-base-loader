"""Entity data model."""

from enum import Enum


class Entity(str, Enum):
    """Type of Entity."""

    ASTEC = "astec"
    MARKET_CAP = "market_cap"
    RETURNS = "returns"
    SHARES_OUT = "shares_out"

    def __repr__(self) -> str:
        return str(self.value)
