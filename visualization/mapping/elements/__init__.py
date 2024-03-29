"""Initializes the abstract MappingElement class used by the Mapping class.

This file describes an abstract class and its equality operators for use by the
rest of the mapping library.

Typical usage example:
class Foo(MappingElement):
    pass
"""

from __future__ import annotations

# imports abstract classes
from abc import ABC, abstractmethod

# imports numpy
import numpy as np


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
        if not isinstance(other, MappingElement):
            raise TypeError(f"Cannot compare MappingElement to {type(other)}")

        # they're not equal if they're not the same type
        if not isinstance(other, type(self)):
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
    def __str__(self) -> str:
        raise NotImplementedError(
            f"Class {type(self)} has not implemented this method yet."
        )


class Distinguishable:
    """Makes an object able to list key differences between itself and another
    object of its type."""

    @abstractmethod
    def diff(self, other) -> str:
        """Creates a string marking the differences between oneself and another
        member of the class.

        Attributes:
            other -- of the same type as self. To be comapred against.

        Returns:
            A string with color-agnostic representation of the differences.
        """
        raise NotImplementedError(f"{type(self)} has not implemented diffstring")

    @abstractmethod
    def blank(self) -> Distinguishable:
        """Creates a "blank" version of the element, signifying a trivial
        implementation of the type element (i.e. does not affect performance
        if omitted from notation).

        Returns:
            A trivial object of type(self)
        """
        raise NotImplementedError(f"{type(self)} has not implemented blank")
