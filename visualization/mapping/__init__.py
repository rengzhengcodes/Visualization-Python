"""Defines the default Mapping class used to represent
hardware mappings.

Typical use case:
mapping = Mapping([Buffer, ForLoop])
"""
# imports type hinting tools
from __future__ import annotations
from typing import Union, Iterable

# imports numpy
import numpy as np

# imports mapping elements
from mapping.elements import MappingElement
from mapping.elements import stores, loops


class Block:
    """Represents an indentation block, caused by a buffer
    level, in the code.

    We do not use buffers to store this info because strict
    buffer instance to buffer instance equality comparison
    should be based on the buffer attributes itself. This
    additional level of abstraction makes that explicit.

    Attributes:
        buffer: The buffer which this level is encapsulated in
        children: The elements that directly belong to this block.
    """

    def __init__(self, buffer: stores.Store) -> None:
        """Inits the Block with the buffer its contained in and a list"""
        self._buffer: stores.Store = buffer
        self._children: list[Union[MappingElement, Block]] = []

    def flatten(self) -> tuple:
        """Returns the block representation as a flattened version of self"""
        # the flattened representation
        flat:list = []

        for elem in self:
            # if it's a block, make that block flatten itself and add it to flat
            if isinstance(elem, Block):
                flat += elem.flatten()
            # else, append the element
            else:
                flat.append(elem)

        return tuple(flat)


    #################
    # ITERATOR FXNS #
    #################

    def __iter__(self) -> Iterable:
        """Makes Block an Iterable."""
        return self

    def __next__(self) -> Union[MappingElement, Block]:
        """Makes block able to iterate"""
        # buffer starts the block
        yield self.buffer

        # the rest of the elements follow
        for element in self.children:
            yield element

        # nothing more to iterate through
        return StopIteration

    ########################
    # BUFFER ACCESSOR FXNS #
    ########################

    @property
    def buffer(self) -> stores.Store:
        """Returns the buffer the Block represents"""
        return self._buffer

    @property
    def level(self) -> int:
        """The block level is the same as the buffer level"""
        return self.buffer.level

    ###########################
    # CHILDREN ACCESSSOR FXNS #
    ###########################

    def children(self) -> tuple:
        """Returns a static copy of all the elements"""
        return tuple(self._children)


class Mapping:
    """Represents a hardware mapping."""

    def __init__(self, elements: Iterable[MappingElement]):
        """Initializes the Mapping, in blocks format"""
        for element in elements:
            if isinstance(element, stores.Store):
                pass
