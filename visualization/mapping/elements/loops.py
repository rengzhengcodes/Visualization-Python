"""This module defines all loop types for a mapping.

Typical usage example:
ForLoop = For('X', 0, 4)
"""


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

    def kindred(self, other: Loop):
        """Implements the kindred method from MappingElement"""
        # can only be kindred if the other is a loop
        if not isinstance(other, Loop):
            return False

        # is kindred if they're iterating over the same dimension
        return self.dim == other.dim

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

    def __init__(self, dim: str, start: int, end: int):
        """Inits the serial loop."""
        super().__init__(dim, start, end)

    def __str__(self):
        return f"for {self._dim} in [{self.start}, {self.end})"


class ParFor(Loop):
    """A mapping element representing a parallel loop."""

    def __init__(self, dim: str, start: int, end: int):
        """Inits the parallel loop."""
        super().__init__(dim, start, end)

    def __str__(self):
        return f"par-for {self.dim} in [{self.start}, {self.end})"
