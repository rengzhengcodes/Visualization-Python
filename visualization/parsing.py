# gets the classes we constructed
from visualization.mapping import *
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
    return mapping_texts

if __name__ == "__main__":
    parse(open("testdata.txt"))
