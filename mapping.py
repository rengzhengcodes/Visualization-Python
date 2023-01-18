from __future__ import annotations
from typing import Iterable, Set

class MappingElement:
    pass

class Loop(MappingElement):
    def __init__(self, dimension: str, start: int, end: int):
        self.dimension = dimension
        self.start = start
        self.end = end

class For(Loop):
    def __init__(self, dimension: str, start: int, end: int):
        super().__init__(dimension, start, end)

    def __eq__(self, other):
        return (isinstance(other, For) and self.dimension == other.dimension
                and self.start == other.start and self.end == other.end)

    def pretty_print(self):
        return f'for {self.dimension} in [{self.start}, {self.end})'

class ParFor(Loop):
    def __init__(self, dimension: str, start: int, end: int):
        super().__init__(dimension, start, end)

    def __eq__(self, other):
        return (isinstance(other, ParFor) and self.dimension == other.dimension
                and self.start == other.start and self.end == other.end)

    def pretty_print(self):
        return f'par-for {self.dimension} in [{self.start}, {self.end})'

class Store(MappingElement):
    def __init__(self, buffer: str, data: Set[str]):
        self.buffer = buffer
        self.data = set(data)

    def __eq__(self, other):
        return (isinstance(other, Store) and self.buffer == other.buffer
                and self.data == other.data)

    def pretty_print(self):
        return f'{self.buffer} holds {self.data}'

class Mapping:
    def __init__(self, elements: Iterable[MappingElement]):
        self.elements = list(elements)

    def __len__(self):
        return len(self.elements)

    def pretty_print(self):
        return '\n'.join(map(lambda e: e.pretty_print(), self.elements))

class MappingDiff:
    def __init__(self):
        raise NotImplementedError()

    def pretty_print(self):
        raise NotImplementedError()

def mapping_diff(mapping1: Mapping, mapping2: Mapping) -> MappingDiff:
    """
    Based on the LCS algorithm:
    https://en.wikipedia.org/wiki/Longest_common_subsequence
    """
    raise NotImplementedError()

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
        Store('L2', {'A', 'B', 'Z'}),
        For('m', 0, 4),
        For('k', 0, 2),
        For('n', 0, 4),
        Store('L1', {'A', 'B', 'Z'}),
        For('m', 0, 4),
        For('n', 0, 4),
        ParFor('k', 0, 8),
        Store('L0', {'A', 'B', 'Z'}),
        For('m', 0, 1),
        For('n', 0, 1),
        For('k', 0, 1)
    ])

    print(mapping.pretty_print())

    other_mapping = Mapping([
        Store('L2', {'A', 'B', 'Z'}),
        For('k', 0, 2),
        For('m', 0, 4),
        For('n', 0, 4),
        Store('L1', {'A', 'B', 'Z'}),
        For('m', 0, 4),
        For('n', 0, 4),
        ParFor('k', 0, 8),
        Store('L0', {'A', 'B', 'Z'}),
        For('m', 0, 1),
        For('n', 0, 1),
        For('k', 0, 1)
    ])

    print(mapping_diff(mapping, other_mapping))
