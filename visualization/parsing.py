# gets the classes we constructed
from mapping import *
# for typehinting
from io import TextIOWrapper
# for finding stuff
import regex as re

def parse(file:TextIOWrapper) -> list: 
    """
    file:TextIOWrapper
        File object pointing to the timeloop printout.
    
    returns:
        A list of mappings included in the printout
    """
    # the entire file
    raw:str = file.read()
    """
    Breaks it up by mapping, which is in 4 line chunks. Source: https://stackoverflow.com/questions/26459838/splitting-a-string-every-n-lines-using-regex
    (?:     # Start a non-capturing group that matches...
    ^       # (from the start of a line)
    .*      # any number of non-newline characters
    $       # (until the end of the line).
    \n?     # Then it matches a newline character, if present.
    ){4}  # It repeats this three times. If there are less than three lines
            # at the end of the string.
    """
    mapping_texts:list = re.compile("(?:^.*$\n?){4}", re.M).findall(raw)
    """
    Splits into separate lines.

    [{dimension},{start},{end};]*  // these are the loops in the mapping (from innermost to outermost)
    [{storage_level}]*             // these are the storage levels
    [{bypass_mask}]*               // read from right to left. each one is a dataspace (1 means stored)
    [{cycles};{energy};]
    """
    mapping_texts = [
                        [dataspace.rstrip(';') # this step is necessary to remove null string from the split due to ending split char
                            for dataspace in data_str.rstrip().split('\n') # this step is necessary to remove null string from the split due to ending split char
                        ] 
                            for data_str in mapping_texts     
                    ]

    dim_info:str
    storage_levels:str
    bypass_masks:str
    data:str
    for [dim_info, storage_levels, bypass_masks, data] in mapping_texts:
        print(dim_info.split(';'))
        # converts the dim_info into a list containing the loops
        dim_info:list = [
                            For(dim, int(start), int(end))
                                for loop in dim_info.split(';') # if we leaving the trailing ; it will split a blank
                                    for [dim, start, end] in [loop.split(',')] # converts to list as split doesn't return a list, just an iterable
                        ]
        # TODO:: implement storage level descriptors to dims
        storage_levels:list = [int(level) for level in storage_levels.split(';')]
        # bypass masks, read left to right TODO::implement bypass descriptors
        bypass_masks = [mask[::-1] for mask in bypass_masks] # reverses direction so indicies line up 
        # extracts performance information. TODO::store performance information in mapping
        data:list = [float(info) for info in data.split(';')]

    return 1 
if __name__ == "__main__":
    print(parse(open("testdata.txt")))
