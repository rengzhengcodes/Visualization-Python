"""Defines all store element types for a mapping.

Typical use case:
L0Buffer = Store(0, ('X'), 0)
"""


class Store(MappingElement):
    """represents levels of storage our mapping has.

    Attributes:
        buffer: The level of the buffer (closeness to compute)
        dataspaces: The dataspaces the buffer contains.
    """

    def __init__(self, buffer: int, dataspaces: tuple[str], bypass: np.uint32 = 0):
        """Inits Store with buffer level, data, and prunes bypass from data"""
        self._buffer: int = buffer

        # the data living in this space, post bypass
        resident_spaces: list = []

        # Take LSB (right-most) bit as index 0 for bypass.
        for index, space in enumerate(dataspaces):
            # checks if this index was bypassed
            if not (bypass >> index) & 0b1:
                # if not, add datspace
                resident_spaces.append(space)

        self._dataspaces: tuple = tuple(resident_spaces)

    ########################
    # BUFFER ACCESSOR FXNS #
    ########################

    @property
    def buffer(self):
        """Getter for self._buffer"""
        return self._buffer

    ############################
    # DATASPACES ACCESSOR FXNS #
    ############################

    @property
    def dataspaces(self):
        """Getter for self._dataspaces"""
        return self._dataspaces
