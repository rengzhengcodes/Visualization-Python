"""This module acts as a server that creates a basic front-end for this
mapping visualization library.

Typical use cases:
    Running this file to create the server.
"""

# visualization libraries
from flask import Flask, render_template
import plotly.express as px
import pandas as pd
import numpy as np

# python markdown to html conversion
from flask_misaka import Misaka

# imports custom mapping class
from mapping import Mapping
from mapping.elements.loops import For, ParFor
from mapping.elements.stores import Store

# creates server
app: Flask = Flask(__name__)
# makes it markdown compliant
Misaka(
    app,  # converts app to markdown
    strikethrough=True,  # allows strikethrough notation
    highlight=True,  # allows highlight notation
    no_indented_code=True,  # disables tabs = code notation
)


# landing page, serves as example graphical page for now
@app.route("/basic")
def basic() -> str:
    """Serves a webapp on the root address that directly compares 2 mappings
    written in code. No justification occuring,
    """
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

    mapping = Mapping(
        [
            Store(2, ("A", "B", "Z")),
            For("m", 0, 4),
            For("k", 0, 2),
            For("n", 0, 4),
            Store(1, ("A", "B", "Z"), np.uint32(0b11)),
            For("m", 0, 4),
            For("n", 0, 4),
            ParFor("k", 0, 8),
            Store(0, ("A", "B", "Z")),
            For("m", 0, 1),
            For("n", 0, 1),
            For("k", 0, 1),
        ]
    )

    other_mapping = Mapping(
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
            For("m", 0, 1),
            For("n", 0, 1),
            ParFor("k", 0, 1),
        ]
    )

    return render_template(
        "mapping.html",
        diffs=(
            mapping.diff(other_mapping),
            other_mapping.diff(mapping),
        ),
        mappings=(mapping, other_mapping),
    )


@app.route("/justify")
def justify() -> str:
    """Very crude visual test for the justification function."""
    mapping = Mapping(
        [
            Store(2, ("A", "B", "Z")),
            For("n", 0, 4),
            Store(1, ("A", "B", "Z"), np.uint32(0b11)),
            Store(0, ("A", "B", "Z")),
            For("m", 0, 1),
            For("k", 0, 1),
        ]
    )
    other_mapping = Mapping(
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
            For("m", 0, 1),
            For("n", 0, 1),
            ParFor("k", 0, 1),
        ]
    )
    # justifies the mappings against each other
    mapping = mapping.justify(other_mapping)
    other_mapping = other_mapping.justify(mapping)

    print(mapping)
    print("#######")
    print(other_mapping)

    return render_template(
        "mapping.html",
        diffs=(
            mapping.diff(other_mapping),
            other_mapping.diff(mapping),
        ),
        mappings=(mapping, other_mapping),
    )


@app.route("/just_complex")
def justify_complex():
    """Crude complex justify test"""
    mapping = Mapping(
        [
            Store(2, ("A", "B", "Z")),
            For("m", 0, 2),
            For("k", 0, 2),
            Store(1, ("A", "B", "Z")),
            ParFor("k", 0, 8),
            For("m", 0, 8),
            Store(0, ("A", "B", "Z")),
            ParFor("k", 0, 1),
            For("n", 0, 1),
        ]
    )

    other_mapping = Mapping(
        [
            Store(2, ("A", "B", "Z")),
            For("m", 0, 2),
            For("n", 0, 4),
            Store(1, ("A", "B", "Z")),
            For("n", 0, 4),
            ParFor("k", 0, 8),
            Store(0, ("A", "B", "Z")),
            For("n", 0, 1),
        ]
    )

    # justifies the mappings against each other
    mapping = mapping.justify(other_mapping)
    other_mapping = other_mapping.justify(mapping)

    print(mapping)
    print("#######")
    print(other_mapping)

    return render_template(
        "mapping.html",
        diffs=(
            mapping.diff(other_mapping),
            other_mapping.diff(mapping),
        ),
        mappings=(mapping, other_mapping),
    )


if __name__ == "__main__":
    app.run(debug=True)
