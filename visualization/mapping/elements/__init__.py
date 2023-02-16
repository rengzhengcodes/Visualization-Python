"""Initializes the abstract MappingElement class used by the
Mapping class.

This file describes an abstract class and its equality operators
for use by the rest of the mapping library.

Typical usage example:
class Foo(MappingElement):
    pass
"""

from __future__ import annotations

# imports abstract classes
from abc import ABC, abstractmethod


class MappingElement:
    """An abstract class representing all mapping elements"""

    def __eq__(self, other: MappingElement) -> bool:
        """Defines strict equality between two mapping elements.

        Args:
            self: The left-hand side of the equality.
            other: The right-hand side of the equality.

        Returns:
            A boolean describing if the two objects are equal
        """
        # makes sure other is a MappingElement
        if not issubclass(MappingElement, other):
            raise TypeError(f"Cannot compare MappingElement to {type(other)}")

        # they're not equal if they're not the same type
        if isinstance(other, type(self)):
            return False

        # they're equal if they share all the same vars
        own_vals: dict = vars(self)
        other_vals: dict = vars(other)

        # goes through all vars to check equality
        for var, val in own_vals.items():
            # check var exists in other
            if var not in other_vals:
                return False
            # checks the values are equal
            if other_vals[var] != val:
                return False

        # if you made it here, all equal, true
        return True

    @abstractmethod
    def kindred(self, other: MappingElement) -> bool:
        """
        Implemented in subclass. Checks to see if the
        two objects are mutations of one another.

        Returns:
            Whether or not two elements are related to
            one another.
        """
        raise NotImplementedError(f"This method is not defined in {type(self)}")
