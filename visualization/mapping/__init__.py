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
from mapping.elements import MappingElement, Distinguishable

# imports classes of elements
from mapping.elements.loops import Loop, For, ParFor
from mapping.elements.stores import Store


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

    def __init__(self, buffer: Store) -> None:
        """Inits the Block with the buffer its contained in and a list"""
        self._buffer: Store = buffer
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
        if isinstance(element, Store):
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
    def buffer(self) -> Store:
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

    @children.setter
    def children(self, orphans: list) -> bool:
        """Sets the children if and if the Block has no children"""
        # if we already have children, don't mutate
        if self.children:
            return False

        # otherwise, adopt the orphans
        for orphan in orphans:
            self.append(orphan)

        return True

    @property
    def loop_dims(self) -> tuple[str]:
        """Returns an ordered list of the dimensions enumerated over"""
        # the list of dimensions
        dims: list = []

        # pulls out the children and their dimensions in order
        for child in self.children:
            dims.append(child.dim)

        return tuple(dims)

    ########################
    # COMPARISON FUNCTIONS #
    ########################

    def justify(self, other: Block) -> Block:
        """Inserts into a copy of self the dims that are located in this Block
        but not the other Block.

        returns the copy of self"""
        # the loops in each Block
        self_loop_dims: tuple[str] = self.loop_dims
        other_loop_dims: tuple[str] = other.loop_dims

        # the loops not contained in both sets
        missing_loops: set[str] = set(self_loop_dims).difference(set(other_loop_dims))
        # the loops not contained in self
        missing_loops.difference_update(self_loop_dims)

        # represents the new block loop order
        new_loops: list[Loop] = list(self.children)

        # inserts the missing loops in the correct relative positions
        loop: str
        for loop in missing_loops:
            # finds its index in other
            other_index: int = other_loop_dims.index(loop)

            # inserts into new loop at index
            new_loops.insert(other_index, other.children[other_index].blank())

        # the new block to be returned
        new_block: Block = Block(self.buffer)
        print(new_loops)

        # sets its children
        new_block.children = new_loops

        return new_block

    def diff(self, other: Block) -> str:
        """Notes the difference between two blocks on the same level"""

        # checks we are doing block to block comparison
        if not isinstance(other, Block):
            raise TypeError(f"Cannot compare {type(other)} to Block.")

        # checks the buffers are of the same level
        assert self.level == other.level, "Cannot compare blocks between levels"

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
                out_string += f"\t{child.diff(other_children[index])}\n"

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

    def __init__(
        self,
        elements: Iterable[MappingElement],
        cycles: int = None,
        energy: float = None,
    ) -> None:
        """Initializes the Mapping, in blocks format

        Attributes:
            cycles: The number of cycles the mapping takes to do the operation.
            energy: The amount of energy needed to do the computation.
        """
        self._cycles: int = cycles
        self._energy: float = energy

        # the indentation blocks in the Mapping
        self._blocks: list[Block] = []

        # the current block we're appending to
        current_block: Block = None

        # goes through all inputted elements
        for element in elements:
            # checks if it's a store, if it is start a new Block
            if isinstance(element, Store):
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

    @blocks.setter
    def blocks(self, blocks: list[Block]) -> None:
        """Sets new blocks if there are no current blocks"""
        if not self.blocks:
            for block in blocks:
                if isinstance(block, Block):
                    self._blocks.append(block)
                else:
                    raise TypeError(f"Expected type Blocks, not {type(block)}")

    ################################
    # CHARACTERISTIC ACCESSOR FXNS #
    ################################

    @property
    def cycles(self) -> int:
        """Gets the number of cycles"""
        return self._cycles

    @cycles.setter
    def cycles(self, cycles: int) -> None:
        """Sets the number of cycles"""
        self._cycles = cycles

    @property
    def energy(self) -> float:
        """Gets the energy cost of the mapping"""
        return self._energy

    @energy.setter
    def energy(self, energy: float) -> None:
        """Sets the energy cost of the mapping"""
        self._energy = energy

    ###################
    # COMPARISON FXNS #
    ###################

    def justify(self, other: Mapping) -> Mapping:
        """Returns a new mapping where all the blocks in self have been justified
        against other."""

        # new blocks the new mapping will have
        justified: list[Block] = []

        # goes through all the blocks in self
        block: Block
        for index, block in enumerate(self.blocks):
            # justifies against the corresponding block in other
            justification: Block = block.justify(other.blocks[index])
            # appends the justified block
            justified.append(justification)

        # initializes a new mapping
        out: Mapping = Mapping([], self.cycles, self.energy)
        # loads in blocks
        out.blocks = justified

        return out

    def diff(self, other: Mapping) -> str:
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
