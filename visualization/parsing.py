# gets the classes we constructed
from mapping.elements.stores import Store
from mapping.elements.loops import For, ParFor
from mapping import Block, Mapping, MappingElement

# for typehinting
from io import TextIOWrapper

# for finding stuff
import regex as re

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
    # Source: https://stackoverflow.com/questions/26459838/splitting-a-string-every-n-lines-using-regex
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


def parse(file: TextIOWrapper) -> list:
    """
    file:TextIOWrapper
        File object pointing to the timeloop printout.

    returns:
        A list of mappings included in the printout
    """
    # the entire file
    raw: str = file.read()
    
    ###
    # Splits into separate lines.

    # [{dimension},{start},{end};]*  // these are the loops in the mapping (from innermost to outermost)
    # [{storage_level}]*             // these are the storage levels
    # [{bypass_mask}]*               // read from right to left. each one is a dataspace (1 means stored)
    # [{cycles};{energy};]
    ###
    mapping_texts = [
        [
            dataspace.rstrip(
                ";"
            )  # this step is necessary to remove null string from the split due to ending split char
            for dataspace in data_str.rstrip().split(
                "\n"
            )  # this step is necessary to remove null string from the split due to ending split char
        ]
        for data_str in mapping_texts
    ]

    # stores all the mappings
    mappings: list = list()

    loop_info: str
    storage_levels: str
    bypass_masks: str
    data: str
    for [loop_info, storage_levels, bypass_masks, data] in mapping_texts:
        # stores the master mapping structure
        mapping: list = list()

        # converts the loop_info into the loops and dumps them in mapping.
        for loop in loop_info.split(";"):
            for dim, start, end in [loop.split(",")]:
                mapping.append(For(dim, int(start), int(end)))

        # gets the indicies of the loops the levels refer to
        storage_levels: list[int] = [int(level) for level in storage_levels.split(";")]
        # creates corresponding level curves and inserts them into the correct position
        for Lval in range(len(storage_levels) - 1, -1, -1):
            mapping.insert(
                storage_levels[Lval],
                Store(Lval, ("A", "B", "Z")),  # don't know what dataspace it stores yet
            )

        # bypass masks, read left to right TODO::implement bypass descriptors
        bypass_masks = [
            mask[::-1] for mask in bypass_masks
        ]  # reverses direction so indicies line up
        # extracts performance information. TODO::store performance information in mapping
        data: list = [float(info) for info in data.split(";")]

        mappings.append(Mapping(mapping))

    return mappings


if __name__ == "__main__":
    for mapping in isolate_mappings(open("testdata.txt").read()):
        print(mapping)