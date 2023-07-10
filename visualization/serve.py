"""This module acts as a server that creates a basic front-end for this
mapping visualization library.

Typical use cases:
    Running this file to create the server.
"""

# Imports memory io for bytes.
from io import TextIOWrapper, BytesIO
import json
import yaml

# Visualization libraries.
from flask import Flask, render_template, redirect, request
import plotly.express as px
import pandas as pd
import numpy as np

# Imports typing for file uploads.
from werkzeug.datastructures import FileStorage

# Python markdown to html conversion.
from flask_misaka import Misaka

# Imports custom mapping class.
from mapping import Mapping
from mapping.elements.loops import For, ParFor
from mapping.elements.stores import Store


# Imports parsing.
from parsing import parse_file

# Creates server.
app: Flask = Flask(__name__)
# Makes server markdown compliant.
Misaka(
    app,                    # converts app to markdown
    strikethrough=True,     # allows strikethrough notation
    highlight=True,         # allows highlight notation
    no_indented_code=True,  # disables tabs = code notation
)


# Landing page, serves as example graphical page for now.
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
            For("k", 0, 8),
            Store(0, ("A", "B", "Z")),
            For("m", 0, 1),
            For("n", 0, 1),
            ParFor("k", 0, 1),
        ]
    )

    return render_template(
        "mapping_to_mapping.html",
        diffs=(
            mapping.diff(other_mapping),
            other_mapping.diff(mapping),
        ),
        mappings=(mapping, other_mapping),
    )


@app.route("/justify_aware")
def justify_aware() -> str:
    """Very crude visual test for the justification function."""
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
            For("k", 0, 8),
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
        "mapping_to_mapping.html",
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
        "mapping_to_mapping.html",
        diffs=(
            mapping.diff(other_mapping),
            other_mapping.diff(mapping),
        ),
        mappings=(mapping, other_mapping),
    )


@app.route("/just_complex")
def justify_complex() -> str:
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
        "mapping_to_mapping.html",
        diffs=(
            mapping.diff(other_mapping),
            other_mapping.diff(mapping),
        ),
        mappings=(mapping, other_mapping),
    )


@app.route("/multi")
def parse() -> str:
    """Parse output tester"""
    # imports test data
    with open("testdata.txt", encoding="utf-8") as testdata:
        mappings: list[Mapping] = parse_file(testdata)

    # generates all the differences
    diffs: tuple[Mapping] = tuple(mapping.diff(mappings[0]) for mapping in mappings)

    return render_template("multi_mapping.html", diffs=diffs, mappings=mappings)


@app.route("/parse", methods=["POST"])
def parse_timeloop() -> str:
    """
    Takes a timeloop input file and parses it before displaying the output.
    Assumes mappings are properly formatted and first mapping in the file
    is the prime mapping to be analyzed.
    """
    # if the form exists
    if "timeloop_output" in request.files:
        # get the test data from the form
        file: FileStorage = request.files["timeloop_output"]

        # parses the data
        mappings: list[Mapping] = parse_file(TextIOWrapper(BytesIO(file.read())))

        # generates all the differences
        diffs: tuple[Mapping] = tuple(mapping.diff(mappings[0]) for mapping in mappings)

        return render_template("multi_mapping.html", diffs=diffs, mappings=mappings)

    # otherwise, stay on the same page
    return redirect(request.referrer)


@app.route("/looptree")
def looptree() -> str:
    """Loops tree visualizer test"""
    # Extracts the YAML looptree raw data.
    looptree_data: dict = yaml.safe_load(open("looptree.yaml", "r", encoding="utf-8"))
    # Extracts the mapping tree.
    mapping: dict = looptree_data["mapping"]
    # Extracts the type of mapping we have. 
    mapping_type: str = mapping["type"]
    # Extracts the mapping tree.
    map_tree: list[dict] = mapping["nodes"]

    return render_template("looptree.html", map_tree=map_tree, mapping_type = mapping_type)

if __name__ == "__main__":
    app.run(debug=True)
