"""This module defines all loop types for a mapping.

Typical usage example:
ForLoop = For('X', 0, 4)
"""
# future annotations
from __future__ import annotations

# imports super classes
from mapping.elements import MappingElement, Distinguishable


class Loop(MappingElement, Distinguishable):
    """A mapping element representing a generic loop.

    Attributes:
        dim: The dimension we're iterating along
        start: Start of iteration.
        end: End of iteration.
    """

    # The general format any printout should be in
    _frame: str = "{loop_type} {dim} in [{start}, {end})"
    # Notes this is a generic loop
    _loop_type: str = "loop"

    def __init__(self, dim: str, start: int, end: int):
        """Inits Loop with dimension, start, and end"""
        assert start < end, f"start:{start} >= end:{end}"
        self._dim: str = dim
        self._start: int = start
        self._end: int = end

    #####################
    # DIM ACCESSOR FXNS #
    #####################

    @property
    def dim(self) -> str:
        """Getter fxn for self._dim"""
        return self._dim

    #######################
    # START ACCESSOR FXNS #
    #######################

    @property
    def start(self) -> str:
        """Getter fxn for self._start"""
        return self._start

    #####################
    # END ACCESSOR FXNS #
    #####################

    @property
    def end(self) -> str:
        """Getter fxn for self._end"""
        return self._end

    ###################
    # COMPARISON FXNS #
    ###################

    def diff(self, other: Loop) -> str:
        """Notes the differences between each loop"""
        if not isinstance(other, Loop):
            raise TypeError(f"{type(other)} cannot be compared with loops")

        # if the two are equal, just return the str
        if self == other:
            # tests that the equality function is true implicitly
            assert str(self) == str(
                other
            ), f"{self} and {other} evaluated as the same but aren't."

            # returns the string, as the two should be the same
            return str(self)

        # tests that the equality function is untrue implicitly
        assert str(self) != str(
            other
        ), f"{self} and {other} evaluated as different but aren't."

        # strings representing the printout variables
        loop_type: str = self._loop_type
        dim: str = str(self.dim)
        start: str = str(self.start)
        end: str = str(self.end)

        # checks if loop type is equal, if not, note
        if not isinstance(self, type(other)):
            loop_type = f"*{loop_type}*"

        # checks if dim is equal, if not, note.
        if self.dim != other.dim:
            dim = f"**{dim}**"

        # checks if start are equal, if not, note whether or not this is is an
        # increase or decrease
        if self.start < other.start:
            start = f"{start} v"
        elif self.start > other.start:
            start = f"{start} ^"

        # does the start check but for end
        if self.end < other.end:
            end = f"{end} v"
        elif self.end > other.end:
            end = f"{end} ^"

        return self._frame.format(loop_type=loop_type, dim=dim, start=start, end=end)

    #########################
    # testing aid functions #
    #########################

    def __str__(self) -> str:
        """Returns a string representation of the loop"""
        return self._frame.format(
            loop_type=self._loop_type, dim=self._dim, start=self._start, end=self._end
        )


class For(Loop):
    """A mapping element representing a serial loop."""

    # string representation of what type of loop this is
    _loop_type = "for"


class ParFor(Loop):
    """A mapping element representing a parallel loop."""

    # string representation of what type of loop this is
    _loop_type = "par-for"
