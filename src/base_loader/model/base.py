"""Abstract model."""

from abc import ABC, abstractmethod
from typing import List, Tuple


class Modeling(ABC):
    """Modeling abstract class."""

    @classmethod
    @abstractmethod
    def build_record(cls, record: List) -> "Modeling":
        """Transforms record into record object.

        Args:
            record: record to be record object.

        Returns:
            Record object for the given entity.
        """

    @abstractmethod
    def as_tuple(self) -> Tuple:
        """Returns object values as a tuple.

        Returns:
            Record object attributes as a tuple.
        """

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        """Returns if record is empty or not."""

    @property
    @abstractmethod
    def is_weekend(self) -> bool:
        """Returns if record is on weekend or not."""
