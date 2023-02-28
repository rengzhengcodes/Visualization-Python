"""This module defines all loop types for a mapping.

Typical usage example:
ForLoop = For('X', 0, 4)
"""
# imports super classes
from mapping.elements import MappingElement


class Loop(MappingElement):
    """A mapping element representing a generic loop.

    Attributes:
        dim: The dimension we're iterating along
        start: Start of iteration.
        end: End of iteration.
    """

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


class For(Loop):
    """A mapping element representing a serial loop."""
    # The general format any printout should be in
    _frame: str = "for {dim} in [{start}, {end})"

    def __init__(self, dim: str, start: int, end: int):
        """Inits the serial loop."""
        super().__init__(dim, start, end)

    #########################
    # testing aid functions #
    #########################

    def __str__(self):
        """Returns a string representation of the loop"""
        return self._frame.format(
            dim = self._dim, start = self._start, end = self._end
        )


class ParFor(Loop):
    """A mapping element representing a parallel loop."""
    # The general format any printout should be in
    _frame: str = "par-for {dim} in [{start}, {end})"

    def __init__(self, dim: str, start: int, end: int):
        """Inits the parallel loop."""
        super().__init__(dim, start, end)

    #########################
    # testing aid functions #
    #########################

    def __str__(self):
        """Returns a stirng representation of the parallel for loop."""
        return self._frame.format(
            dim = self._dim, start = self._start, end = self._end
        )
