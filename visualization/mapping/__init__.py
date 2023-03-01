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

# imports all of elements
from mapping.elements import MappingElement, Distinguishable, stores


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
        self._children: list[MappingElement] = []

    def flatten(self) -> tuple:
        """Returns the block representation as a flattened version of self"""
        # the flattened representation of the block
        flat: list = [self.buffer] + list(self.children)

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

    def append(self, element: MappingElement) -> None:
        """Appends a new Block or non-store MappingElement to the list"""

        # checks for stores that should be in Blocks
        if isinstance(element, stores.Store):
            raise TypeError("Inserted a Store. This should be inside a new Block")

        # checks we are appending a MappingElement
        if not isinstance(element, MappingElement):
            raise TypeError(f"Inserted {type(element)}, which is not a MappingElement")

        # appends the element to children
        self._children.append(element)

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

    @property
    def children(self) -> tuple:
        """Returns a static copy of all the elements"""
        return tuple(self._children)

    ########################
    # COMPARISON FUNCTIONS #
    ########################

    def diff(self, other:Block) -> str:
        """Notes the difference between two blocks on the same level"""
        
        # checks we are doing block to block comparison
        if not isinstance(other, Block):
            raise TypeError(f"Cannot compare {type(other)} to Block.")

        # checks the buffers are of the same level
        assert self.level == other.level, f"Cannot compare blocks between levels"

        ## synthesizes the diffstring ##

        # the children of the other buffer
        other_children: tuple[MappingElement] = other.children

        # string we're outputting; we don't do any comparison checks on the buffer
        # as we already note the bypasses.
        out_string: str = f"{self.buffer}\n"

        # adds the comparison of the non-buffer elements, indented
        for index, child in enumerate(self.children):
            
            # checks that the child is Distinguishable
            if isinstance(child, Distinguishable):
                # if so, check the difference between the corresponding children
                out_string += f"\t{child.diffstring(other_children[index])}\n"
            
            else:
                # otherwise, just add the child
                out_string += f"\t{child}\n"
        
        return out_string

    #########################
    # testing aid functions #
    #########################

    def __str__(self) -> str:
        """returns a string representation of the Block"""

        # the string we are outputting
        out_string: str = f"{self.buffer}\n"

        # adds the non-buffer elements, indented
        for child in self.children:
            out_string += f"\t{child}\n"

        return out_string


class Mapping:
    """Represents a hardware mapping."""

    def __init__(self, elements: Iterable[MappingElement]) -> None:
        """Initializes the Mapping, in blocks format"""

        # the indentation blocks in the Mapping
        self._blocks: list[Block] = []

        # the current block we're appending to
        current_block: Block = None

        # goes through all inputted elements
        for element in elements:
            # checks if it's a store, if it is start a new Block
            if isinstance(element, stores.Store):
                # creates the new block
                current_block: Block = Block(element)
                # appends it to the list of blocks
                self._blocks.append(current_block)

            # otherwise, add the current element to the current block
            elif isinstance(element, MappingElement):
                current_block.append(element)

            # if it's not a mapping element, what went wrong
            else:
                raise TypeError(f"{type(element)} is not a MappingElement")

    ########################
    # BLOCKS ACCESSOR FXNS #
    ########################

    @property
    def blocks(self) -> tuple[Block]:
        """Returns a tuple of all the blocks currently contained"""
        return tuple(self._blocks)

    ###################
    # COMPARISON FXNS #
    ###################

    def diff(self, other:Mapping) -> str:
        """Notes the differences between two mappings"""
        
        # checks other input type
        if not isinstance(other, Mapping):
            raise TypeError(f"{type(other)} cannot be compared with Mapping")

        ## synthesizes the diffstring ##

        # the blocks of the other mapping
        other_blocks: tuple[Block] = other.blocks

        # the string we're outputting
        out_string: str = ""

        # adds all the blocks and their differences individually
        for index, block in enumerate(self.blocks):
            out_string += f"{block.diff(other_blocks[index])}\n"
        
        return out_string

    #########################
    # testing aid functions #
    #########################

    def __str__(self) -> str:
        """Converts the mapping into a printable string"""

        # the string we are outputting
        out_string: str = ""

        # adds all the blocks individually
        for block in self.blocks:
            out_string += f"{block}\n"

        return out_string
