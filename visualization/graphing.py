from copy import deepcopy
from typing import *

# defines the numeric data type for type hinting
numeric = Union[float, int]

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import *

# np.random.seed(42)

# display conditions
width = 1

# thing's we're trying to measure generally, versus what we need to map to see them
categories = {"Capacity": ["L1", "L2"], "Access Count": ["Read", "Write", "Fill"]}


def generate_random_data(data_points: int) -> tuple:
    """
    Generates random data of the type Timeloop will provide.

    data_points:
        The number of data points we want to get.
    """
    # the list that stores the data point dictionary.
    data = list()

    for i in range(data_points):
        # randomly generates data point
        data_point = {
            "A": {  # A is the component
                "Capacity": {  # Capacity is the category
                    "L1": np.random.randint(
                        50, 100
                    ),  # L1 is the label, the random is the value
                    "L2": np.random.randint(50, 100),
                },
                "Access Count": {
                    "Read": np.random.randint(50, 100),
                    "Write": np.random.randint(50, 100),
                    "Fill": np.random.randint(50, 100),
                },
            },
            "B": {
                "Capacity": {
                    "L1": np.random.randint(50, 100),
                    "L2": np.random.randint(50, 100),
                },
                "Access Count": {
                    "Read": np.random.randint(50, 100),
                    "Write": np.random.randint(50, 100),
                    "Fill": np.random.randint(50, 100),
                },
            },
            "C": {
                "Capacity": {
                    "L1": np.random.randint(50, 100),
                    "L2": np.random.randint(50, 100),
                },
                "Access Count": {
                    "Read": np.random.randint(50, 100),
                    "Write": np.random.randint(50, 100),
                    "Fill": np.random.randint(50, 100),
                },
            },
        }

        data.append(data_point)

    return tuple(data)


# Data on the effect of each process (?) on the measured variables.
generated_data: tuple
generated_data = generate_random_data(5)


def make_data_percentage(data: Iterable = generated_data) -> tuple:
    """
    Takes all the data and preprocesses it so that they are in terms of the max value (100%).

    data:
        An iterable containing all the datapoints we want to normalize over
    """
    # makes a copy of the old data
    data = deepcopy(data)
    # a dictionary storing the largest value in any category across all datapoints in data
    largest_in_category: dict
    largest_in_category = dict()

    # loads all the categories and their respective subcategories (labels) into the dictionary; assumes all data is rectangular
    example_datapoint = data[0]
    example_component = tuple(example_datapoint.keys())[0]
    for category, metric_data in example_datapoint[example_component].items():
        # the dictionary is to store subcomponents of the category data
        largest_in_category[category] = dict()
        for label in metric_data.keys():
            # since all metrics we're looking at are whole numbers, we can initalize all max values as 0 for later comparison.
            largest_in_category[category][label] = 0

    for datapoint in data:
        # dictionary that stores the running sum of each category across all components
        running_sum: dict
        running_sum = dict()

        # pulls the metric data for all components
        for metric_data in datapoint.values():
            # pulls the subdata for all labels to add together
            for category, values in metric_data.items():
                # hodge-podge solution to making sure dict doesn't get reinstatiated. You should proabably just make a key-copy of the largest-sum dict but this works for now.
                if category not in running_sum.keys():
                    running_sum[category] = dict()

                # running sum among all the components in a category
                for label, value in values.items():
                    # instantiates a value if there is no value there
                    if label not in running_sum[category].keys():
                        running_sum[category][label] = 0
                    running_sum[category][label] += value

        # determines max by checking if the values in running sum are greater than the current values of largest_in_category
        for category, values in running_sum.items():
            for label, value in values.items():
                if running_sum[category][label] > largest_in_category[category][label]:
                    largest_in_category[category][label] = running_sum[category][label]

    # uses largest in category to normalize all the data
    for datapoint in data:
        for component, metric_data in datapoint.items():
            for category, values in metric_data.items():
                for label in values.keys():
                    # converts to percentage
                    datapoint[component][category][label] *= 100
                    datapoint[component][category][label] /= largest_in_category[
                        category
                    ][label]

    return data


normalized_data = make_data_percentage()
# print(normalized_data)


def graph_category(category: str, data: tuple = generated_data) -> None:
    """
    Generates a Graph Based on the Category Given

    category:
        the category you want graphed
    """
    # calculates the number of mappings and determine number of plots needed
    number_of_mappings = len(data)
    # creates the figure and the subplots
    fig, subplots = plt.subplots(1, number_of_mappings)

    for i in range(number_of_mappings):
        subplot = subplots[i]
        mapping_data = data[i]
        # Calculates the amount of bars you need. Assumes all components have even data for all categories.
        category_size = len(
            mapping_data[tuple(mapping_data.keys())[0]][category]
        )  # accesses first component in memory, then checks the number of elements describing that category in component.
        index = np.arange(
            category_size
        )  # a list representing all the elements in the category.

        # the dictionary storing the bar contribution for each component
        plots = dict()
        # the bottom of where the bar contribution should be, so that it starts when the last contribution stops
        bottom_val = np.array([0.0] * category_size)

        # accesses all the metrics data for each component
        metric_data: dict
        for component, metric_data in mapping_data.items():
            # Creates the plots for each component
            plots[component] = subplot.bar(
                index, tuple(metric_data[category].values()), width, bottom=bottom_val
            )
            bottom_val += np.array(tuple(metric_data[category].values()))

        # Show title tick marks
        subplot.set_title(f"Mapping {i + 1}")
        subplot.set_ylabel(category)
        subplot.set_xticks(
            index, tuple(mapping_data[tuple(mapping_data.keys())[0]][category].keys())
        )
        subplot.set_yticks(np.arange(0, 301, 100))
        subplot.legend(
            tuple([plot[0] for plot in plots.values()]), tuple(mapping_data.keys())
        )

    fig.suptitle("Relation of Structure to " + category)


def flatten_data_point(datapoint: dict) -> dict:
    """
    Takes the data from a datapoint and flattens it into just a key-pair interaction

    datapoint:
        A datapoint like the ones generated above

    Returns:
        A flattened datapoint of the form:
        {
            "Component": {
                "Capacity Alpha": int,
                "L1 Read": int,
                "L1 Write": int,
                etc etc
            }
        }
    """

    return pd.json_normalize(datapoint, sep=" ").to_dict(orient="records")[0]


def graph_unified_mapping(data: tuple = normalized_data) -> None:
    """
    Graphs all the data for a mapping in relation to the max amount in each category for a dataset (set as 100% in the scaling).

    data:
        The data collected from time loop, processed by the normalization function.
    """

    # calculates the number of mappings needed to determine the number of plots needed
    number_of_mappings = len(data)
    # creates the figure and subplots
    fig, subplots = plt.subplots(1, number_of_mappings)

    for i in range(number_of_mappings):
        subplot = subplots[i]
        mapping_data = data[i]

        # the dictionary containing each bar plot.
        plots = dict()
        # the bottom offset for the graphs
        bottom_val: np.NDArray
        bottom_val = None

        for component, values in mapping_data.items():
            # gets the 1D representation of the data so we don't have to do more processing of the data.
            values = flatten_data_point(values)
            # gets the number of vertical bars we need
            category_size = len(values)
            # a list representing the bar count; numerical designators for each bar which we will label later
            index = np.arange(category_size)
            # the bottom of where the bar contribution should be for the next component
            if (
                bottom_val is None
            ):  # shoddy workaround again to avoid reinstantiation of the variable
                bottom_val = np.array([0.0] * category_size)

            # creates the bars for a given component in the mapping
            plots[component] = subplot.bar(
                index, tuple(values.values()), width, bottom=bottom_val
            )
            # updates bottom_val to the new bottom for the next thing to display
            bottom_val += np.array(tuple(values.values()))

        # shows titles and tick marks
        subplot.set_title(f"Mapping {i + 1}")
        subplot.set_ylabel("Percentage of Max")
        subplot.set_xticks(index, tuple(values.keys()), rotation="vertical")
        subplot.set_yticks(np.arange(0, 101, 100))
        subplot.legend(
            tuple([plot[0] for plot in plots.values()]), tuple(mapping_data.keys())
        )
        subplot.set_ylim((0, 100))

    fig.suptitle("Relation of Structure to Metrics")


"""
def graph_mapping(data: tuple = generated_data) -> None:
    \"""
    Takes in all the mapping data and generates a radar data plot for each mapping.
    data:
        The data collected from Timeloop.
    \"""
    # defines the first element in the dataset, which we assume is of equal shape to the other pieces of data.
    example_datapoint = data[0]
    # calculates evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, len(tuple(example_datapoint.values())[0]
"""

# graph_category("Capacity", normalized_data)
graph_category("Capacity")
graph_category("Access Count")
graph_unified_mapping()

plt.show()
