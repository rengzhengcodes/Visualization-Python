# imports module classes
from __init__ import *

# visualization libraries
from flask import Flask, render_template
import plotly.express as px
import pandas as pd
# python string to html conversion
from html import escape

app:Flask = Flask(__name__)

# landing page, serves as example graphical page for now
@app.route('/')
def graph():
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

    diff:MappingDiff = MappingDiff(mapping, other_mapping)
    print(diff)
    
    return render_template(
        "mapping.html",
        Fore = Fore,
        mapping_1 = str(diff),
        example_2 = "test2"
    )


if __name__ == '__main__':
    app.run(debug=True)