"""Defines the default Mapping class used to represent
hardware mappings.

Typical use case:
mapping = Mapping([Buffer, ForLoop])
"""
# imports numpy
import numpy as np

# imports mapping elements
from mapping.elements import *

class Block():
    """Represents an indentation block, caused by a buffer
    level, in the code.

    We do not use buffers to store this info because strict
    buffer instance to buffer instance equality comparison
    should be based on the buffer attributes itself. This
    additional level of abstraction makes that explicit.

    Attributes:
        buffer: The buffer which this level is encapsulated in
        elements: The elements that directly belong to this block.
    """
    
    def __init__(self, buffer: store.Buffer):
        """Inits the Block with the buffer its contained in"""
        self._buffer:store.Buffer = buffer
    
    def 
    


class Mapping():
    """Represents a hardware mapping.
    """

    def __init__(self, elements:Iterable[MappingElement]):
        """Initializes the Mapping, in blocks format"""
        for element in elements:
            if isinstance(element, store.Buffer):


        
