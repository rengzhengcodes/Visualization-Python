class Loop(MappingElement):
    """A mapping element representing a generic loop.

    Attributes:
        dim: The dimension we're iterating along
        start: Start of iteration.
        end: End of iteration.
    """

    def __init__(self, dim:str, start:int, end:int):
        """Inits Loop with dimension, start, and end"""
        self.dim:str = dim
        self.start:int = start
        self.end:int = end

class For(Loop):
    """A mapping element representing a serial loop.
    """

    def __init__(self, dim:str, start:int, end:int):
        """Inits the serial loop.
        """
        super(dim, start, end)

class ParFor(Loop):
    """A mapping element representing a parallel loop.
    """

    def __init__(self, dim:str, start:int, end:int):
        """Inits the parallel loop.
        """
        super(dim, start, end)