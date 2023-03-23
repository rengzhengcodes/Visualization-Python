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
            [
                tuple(
                    filter(
                        bool,  # keep split info if non-empty
                        tuple(
                            dataline.split(";")
                        ),  # splits separate components of line
                    )
                )
                for dataline in filter(
                    bool,  # keeps line if non-empty
                    isolated_mapping.split("\n"),  # splits each line in mapping string
                )
            ]
        )
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
    # reads in the raw output file from timeloop
    raw: str = file.read()

    # isolates each mapping in the raw data
    isolated_mappings: list[str] = isolate_mappings(raw)

    # processes each mapping string into more granular subcomponents
    preprocessed_mappings: list[list] = preprocess_mappings(isolated_mappings)

    # stores all the mappings we will initialize
    mappings: list = list()

    # goes through all the pre processed mappings
    loop_info: list
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
    # isolates mappings in test input
    isolated_mappings: list[str] = isolate_mappings(open("testdata.txt").read())
    # test prints
    for mapping in isolate_mappings(open("testdata.txt").read()):
        print(mapping)

    # preprocesses the isolated mappings
    preprocessed_mappings: list[tuple[tuple]] = preprocess_mappings(isolated_mappings)
    # debug prints
    for mapping in preprocessed_mappings:
        print(mapping)
