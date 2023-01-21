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
    mapping_texts = [data_str.split('\n') for data_str in mapping_texts]
    return mapping_texts

if __name__ == "__main__":
    print(parse(open("testdata.txt")))
