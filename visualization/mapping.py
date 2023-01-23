from __future__ import annotations
# for coloring differences in terminal
from colorama import Fore
# type hinting library
from typing import Iterable, Set, Any
# imports parsing
import parsing

# defines the print width
print_width:int = 25

class MappingElement:
    pass

class Loop(MappingElement):
    def __init__(self, dimension: str, start: int, end: int):
        # variable name of dimension e.g. I, J, K
        self.dimension:str = dimension
        # start of iteration
        self.start:int = start
        # end of iteration
        self.end:int = end

class For(Loop):
    def __init__(self, dimension: str, start: int, end: int):
        super().__init__(dimension, start, end)

    def __eq__(self, other:Any) -> bool:
        """
        Checks for functional but not strict identity between objects.
        """
        return (isinstance(other, For) and self.dimension == other.dimension
                and self.start == other.start and self.end == other.end)

    def __str__(self):
        """
        Returns a pretty print string for debugging.
        """
        return f'for {self.dimension} in [{self.start}, {self.end})'

    def __repr__(self):
        """
        Functional representation. Currently set to __str__
        """
        return str(self)

class ParFor(Loop):
    def __init__(self, dimension: str, start: int, end: int):
        super().__init__(dimension, start, end)

    def __eq__(self, other) -> bool:
        """
        Checks for functional but not strict identity between objects.
        """
        return (isinstance(other, ParFor) and self.dimension == other.dimension
                and self.start == other.start and self.end == other.end)

    def __str__(self) -> str:
        """
        Returns a pretty, printable method for debugging
        """
        return f'par-for {self.dimension} in [{self.start}, {self.end})'

class Store(MappingElement):
    def __init__(self, buffer: int, data: Set[str]):
        # buffer level
        self.buffer:int = buffer
        # contained data
        self.data = set(data)

    """
    Comparison operators defined below
    """

    def __eq__(self, other:Any) -> bool:
        """
        Checks for functional but not strict identity between objects.
        """
        return (isinstance(other, Store) and self.buffer == other.buffer
                and self.data == other.data)

    def __lt__(self, other:Store) -> bool:
        """
        Checks if self is less than other.
        """
        assert isinstance(other, Store)
        return self.buffer < other.buffer

    def __str__(self):
        """
        Returns a pretty, printable method for debugging
        """
        return f'L{self.buffer} holds {self.data}'

class Mapping:
    def __init__(self, elements: Iterable[MappingElement]):
        self.elements:list[MappingElement] = list(elements)

    def __len__(self):
        """
        Returns the number of elements in a mapping
        """
        return len(self.elements)

    def __str__(self) -> str:
        """
        Returns a pretty, printable method for debugging
        """
        return '\n'.join(map(lambda e: e.__str__(), self.elements))
    
    def __repr__(self) -> str:
        return str(self)

class MappingDiff:
    class Diff:
        def __init__(self, e1:MappingElement, e2:MappingElement):
            assert type(e1) == type(e2)
            # first mapping element (original)
            self.e1:MappingElement = e1
            # second mapping element (different)
            self.e2:MappingElement = e2
            # differences between the two. Uses a dictionary as we don't know what mapping elements are being entered
            self.differences:dict[str:bool] = dict()

            """
            Iterates through all the mapping variables to spot the differences.
            """
            # pulls out the specific dictionaries representing variables for each element
            v1:dict = vars(e1)
            v2:dict = vars(e2)
            
            # makes sure the two have equal keys
            assert v1.keys() == v2.keys()

            for var in v1.keys():
                # sets the variables to if they correspond
                self.differences[var] = v1[var] != v2[var]
        
        def __str__(self):
            raise NotImplementedError("Coming soon.")

    def __init__(self, m1:Mapping, m2:Mapping):
        # first mapping (original)
        self.m1:Mapping = m1
        # second mapping (different)
        self.m2:Mapping = m2
        # tracks the differences between the two
        self.differences:list[bool] = list()

        """
        Identifies the differing elements between the two through iterating through map elements
        """
        # for now assume they're of equal length
        assert len(m1) == len(m2)
        for i in range(len(m1)):
            # pulls out the elements in question for readability of code
            e1:MappingElement = m1.elements[i]
            e2:MappingElement = m2.elements[i]

            # if elems not equal, mark in differences that they're not equal
            if e1 != e2:
                self.differences.append(MappingDiff.Diff(e1, e2))
            else:
                self.differences.append(False)



    def __str__(self) -> str:
        string:str = ""
        for i in range(len(self.m1.elements)):
            if self.differences[i]:
                # highlights the differences between the two, https://docs.python.org/3/library/string.html#formatstrings
                string += f"{Fore.RED}{str(self.m1.elements[i])[0:print_width]:{print_width}s} | {str(self.m2.elements[i])[0:print_width]:{print_width}s}{Fore.RESET}\n"
            else:
                string += f"{str(self.m1.elements[i])[0:print_width]:{print_width}s} | {str(self.m2.elements[i])[0:print_width]:{print_width}s}\n"
        
        return string

if __name__ == '__main__':
    # A Simple Example
    # 
    # Matrix multiplication: Z[m,n] := A[m,k] B[k,n]
    #
    # Mapping:
    # --- L2
    # for m in [0,4)
    # for k in [0,2)
    # for n in [0,4)
    # --- L1
    # for m in [0,4)
    # for n in [0,4)
    # par-for k in [0,8)
    # --- L0
    # for m in [0,1)
    # for n in [0,1)
    # for k in [0,1)

    mapping = Mapping([
        Store(2, {'A', 'B', 'Z'}),
        For('m', 0, 4),
        For('k', 0, 2),
        For('n', 0, 4),
        Store(1, {'A', 'B', 'Z'}),
        For('m', 0, 4),
        For('n', 0, 4),
        ParFor('k', 0, 8),
        Store(0, {'A', 'B', 'Z'}),
        For('m', 0, 1),
        For('n', 0, 1),
        For('k', 0, 1)
    ])

    print(mapping)
    print("######")

    other_mapping = Mapping([
        Store(2, {'A', 'B', 'Z'}),
        For('k', 0, 2),
        For('m', 0, 4),
        For('n', 0, 4),
        Store(1, {'A', 'B', 'Z'}),
        For('m', 0, 4),
        For('n', 0, 4),
        ParFor('k', 0, 8),
        Store(0, {'A', 'B', 'Z'}),
        For('m', 0, 1),
        For('n', 0, 1),
        For('k', 0, 1)
    ])

    print(MappingDiff(mapping, other_mapping))
