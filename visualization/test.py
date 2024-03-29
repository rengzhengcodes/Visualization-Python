"""Run this module to conduct a quick and dirty visual inspection of all the
mapping functionality.
"""

# imports numpy
import numpy as np

# imports all the mapping elements
from mapping import Mapping
from mapping.elements.stores import Store
from mapping.elements.loops import For, ParFor

mapping1 = Mapping(
    [
        Store(2, ("A", "B", "Z")),
        For("m", 0, 4),
        For("k", 0, 2),
        For("n", 0, 4),
        Store(1, ("A", "B", "Z"), np.uint32(int("11", base=2))),
        For("m", 0, 4),
        For("n", 0, 4),
        ParFor("k", 0, 8),
        Store(0, ("A", "B", "Z")),
        For("m", 0, 1),
        For("n", 0, 1),
        For("k", 0, 1),
    ]
)

# print(mapping)
# print("######")

mapping2 = Mapping(
    [
        Store(2, ("A", "B", "Z")),
        For("k", 0, 2),
        For("m", 0, 2),
        For("n", 0, 4),
        Store(1, ("A", "B", "Z")),
        For("m", 0, 8),
        For("n", 0, 4),
        ParFor("k", 0, 8),
        Store(0, ("A", "B", "Z")),
        For("n", 0, 1),
        For("k", 0, 1),
        ParFor("m", 0, 1),
    ]
)

print("# Mapping 1")
print(mapping1)
print("# Mapping 2")
print(mapping2)
print("# Mapping1 in comparison to Mapping2")
print(mapping1.diff(mapping2))
print("# Mapping2 in comparison to Mapping1")
print(mapping2.diff(mapping1))

print(ParFor("m", 0, 423).blank())