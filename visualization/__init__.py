# postponed type hinting
from __future__ import annotations
# for coloring differences in terminal
from colorama import Fore
# type hinting library
from typing import Iterable, Set, Any

# defines the print width
print_width:int = 50

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
        return '\n'.join(map(lambda e: str(e), self.elements))
    
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
        # keeps track of the indentation level
        indent_level:int = 0
        # The char used to fill for indent
        fillchar:str = '  '

        # assembles string
        for i in range(len(self.m1.elements)):
            # checks if a difference exists
            if self.differences[i]:
                # highlights the differences between the two, https://docs.python.org/3/library/string.html#formatstrings
                string += (
                    Fore.RED + 
                    f"{(fillchar*indent_level + str(self.m1.elements[i]))[0:print_width]:{print_width}s}" + "|" + 
                    f"{(fillchar*indent_level + str(self.m2.elements[i]))[0:print_width]:{print_width}s}" + f"{Fore.RESET}\n"
                )
            else:
                string += (
                        f"{(fillchar*indent_level + str(self.m1.elements[i]))[0:print_width]:{print_width}s}" + "|" + 
                        f"{(fillchar*indent_level + str(self.m2.elements[i]))[0:print_width]:{print_width}s}\n"
                    )
            # if it's a store, increase indentation by 1
            if isinstance(self.m1.elements[i], Store):
                indent_level += 1

        return string.rstrip()