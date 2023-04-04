"""Defines all store element types for a mapping.

Typical use case:
L0Buffer = Store(0, ('X'), 0)
"""

# imports numpy
import numpy as np

# imports super class structure
from mapping.elements import MappingElement


class Store(MappingElement):
    """represents levels of storage our mapping has.

    Attributes:
        level: The level of the store (closeness to compute)
        dataspaces: The dataspaces the buffer contains.
    """

    # The general format any printout should be in
    _frame: str = "buffer {level} stores {dataspaces}"

    def __init__(self, level: int, dataspaces: tuple[str], bypass: np.uint32 = 0):
        """Inits Store with buffer level, data, and prunes bypass from data"""
        self._level: int = level

        # the data living in this space, post bypass
        resident_spaces: list = []

        # Take LSB (right-most) bit as index 0 for bypass.
        for index, space in enumerate(dataspaces):
            # checks if this index was bypassed
            if not (bypass >> index) & 0b1:
                # if not, add dataspace
                resident_spaces.append(space)

            # if it was, mark that the dataspace was bypassed with ~ ~ for strikethrough
            else:
                resident_spaces.append(f"==~~{space}~~==")

        self._dataspaces: tuple = tuple(resident_spaces)

    #########################
    # testing aid functions #
    #########################

    def __str__(self) -> str:
        """String representation of the Store"""

        # builds the string for dataspaces so we don't have annoying "" in print
        dataspace_str: str = "("

        # adds all the dataspaces
        for dataspace in self.dataspaces:
            dataspace_str += f"{dataspace}, "

        # removes ", " from the end of the string printing and closes paren
        dataspace_str = f"{dataspace_str.rstrip(', ')})"

        return self._frame.format(level=self.level, dataspaces=dataspace_str)

    ########################
    # BUFFER ACCESSOR FXNS #
    ########################

    @property
    def level(self):
        """Getter for self._buffer"""
        return self._level

    ############################
    # DATASPACES ACCESSOR FXNS #
    ############################

    @property
    def dataspaces(self):
        """Getter for self._dataspaces"""
        return self._dataspaces
