"""Parses mappings from a description in a file outputted by a timeloop hack.
The file is of the form {{INSERT DESCRIPTION HERE}}

Typical use case:
    mappings: list[Mapping] = parse_file(open("path/to/file"))
"""
# for typehinting
from io import TextIOWrapper

# imports numpy for bypass masks
import numpy as np

# for finding stuff
import regex as re

# gets the classes we constructed
from mapping.elements.stores import Store
from mapping.elements.loops import For
from mapping import Mapping


def isolate_mappings(raw: str) -> list[str]:
    """Takes a string of the form found in testdata.txt and breaks it into a list
    of strings that only contain the information for one mapping.

    Attributes:
        raw: A string representing the mappings the user wants the program to
        compare

    Returns:
        A list of strings, where each string is exactly 1 mapping.
    """
    ###
    # Breaks it up by mapping, which is in 4 line chunks.
    # Source:
    # https://stackoverflow.com/questions/26459838/splitting-a-string-every-n-lines-using-regex
    # (?:     # Start a non-capturing group that matches...
    # ^       # (from the start of a line)
    # .*      # any number of non-newline characters
    # $       # (until the end of the line).
    # \n?     # Then it matches a newline character, if present.
    # ){4}  # It repeats this three times. If there are less than three lines
    #         # at the end of the string.
    ###

    mapping_texts: list = re.compile("(?:^.*$\n?){4}", re.M).findall(raw)

    return mapping_texts


def preprocess_mappings(isolated: list[str]) -> list[tuple[tuple]]:
    """Takes an output from isolate_mappings and then forms a list of tuples of
    tuples. Each outer tuple has 4 fields:
    [
        loops,          // these are the loops in the mapping (from innermost to outermost)
        storage_levels, // these are the storage levels
        bypass_masks,   // read from right to left. one per level (1 means stored in level)
        performance_metrics
    ]

    Attributes:
        isolated: Of the form of the output from isolate_mappings

    Returns:
        A list of tuples of tuples, where the outermost tuple represents a mapping
        and the innermost tuple representing a specific aspect of the mapping, as
        listed above.
    """
    # processes each line of all isolated mappings and then splits the separate
    # components per line
    preprocessed_mappings: list = [
        tuple(
            tuple(
                # writes components if not empty string from split
                component
                for component in dataline.split(";")
                if component
            )
            # processes dataline if not empty line from split
            for dataline in isolated_mapping.split("\n")
            if dataline
        )
        # goes through all mappings
        for isolated_mapping in isolated
    ]

    return preprocessed_mappings


def parse_file(file: TextIOWrapper) -> list:
    """
    file:TextIOWrapper
        File object pointing to the timeloop printout.

    returns:
        A list of mappings included in the printout
    """
    # stores all the mappings we will initialize
    mappings: list = []

    # goes through all the preprocessed mappings
    loops: tuple[str]           # all the loops in a mapping
    storage_indices: tuple[str] # the index of the first loop a Store contains
    bypass_masks: tuple[str]    # the bypass masks per Store
    metrics: tuple[str]         # mapping performance data
    for loops, storage_indices, bypass_masks, metrics in preprocess_mappings(
        # isolates each mapping in the raw data
        isolate_mappings(
            # reads in the raw output file from timeloop
            file.read()
        )
    ):
        # stores the master mapping structure
        mapping: list = []

        # iterates through all loops
        loop: str
        for loop in loops:
            # splits the loop representation into component parts
            dim: str
            start: str
            end: str
            dim, start, end = loop.split(",")

            # instantiates a corresponding loop and appends to mapping
            mapping.append(For(dim, int(start), int(end)))

        # gets the index of the loop each Store first contains
        storage_indices: list[int] = [int(level) for level in storage_indices]

        # goes through all stores in reverse order and inserts them, reverse so
        # we don't need to worry about later elements shifting in list.
        store_level: int  # index we're at in iteration, corresponds to Store level
        loop_index: int  # the index of the loop this Store first contains
        for store_level, loop_index in reversed(tuple(enumerate(storage_indices))):
            mapping.insert(
                # inserts at loop index as Store has to come before a Loop to contain it
                loop_index,
                # instantiates the corresponding Store
                Store(
                    # default variables
                    store_level, ("A", "B", "Z"),
                    # grabs the bypass corresponding to this Store
                    np.uint32(bypass_masks[store_level])
            ),
            )

        # pulls out cycles and energy data
        cycles, energy = metrics
        # ints the metrics
        cycles: int = int(cycles)
        energy: int = int(energy)

        mappings.append(Mapping(mapping, cycles, energy))

    return mappings


if __name__ == "__main__":
    # isolates mappings in test input
    with open("testdata.txt", "r", encoding="utf-8") as testdata:
        iso: list[str] = isolate_mappings(testdata.read())
    # test prints
    for m in iso:
        print(m)

    # preprocesses the isolated mappings
    preprocessed: list[tuple[tuple]] = preprocess_mappings(iso)
    # debug prints
    for m in preprocessed:
        print(m)
