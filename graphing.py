from typing import Union
# defines the numeric data type for type hinting
numeric = Union[float, int]

import matplotlib.pyplot as plt
import numpy as np
from math import *

#np.random.seed(42)

# display conditions
width = 1

# thing's we're trying to measure generally, versus what we need to map to see them
categories = {
    "Capacity": ["L1", "L2"],
    "Access Count": ["Read", "Write", "Fill"]
}

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
            'A': { # A is the component
                "Capacity": { # Capacity is the category
                    "L1": np.random.randint(50, 100), # L1 is the label, the random is the value
                    "L2": np.random.randint(50, 100),
                },
                "Access Count": {
                    "Read": np.random.randint(50, 100),
                    "Write": np.random.randint(50, 100),
                    "Fill": np.random.randint(50, 100),
                }
            },
            'B': {
                "Capacity": {
                    "L1": np.random.randint(50, 100),
                    "L2": np.random.randint(50, 100),
                },
                "Access Count": {
                    "Read": np.random.randint(50, 100),
                    "Write": np.random.randint(50, 100),
                    "Fill": np.random.randint(50, 100),
                }
            },
            'C': {
                "Capacity": {
                    "L1": np.random.randint(50, 100),
                    "L2": np.random.randint(50, 100),
                },
                "Access Count": {
                    "Read": np.random.randint(50, 100),
                    "Write": np.random.randint(50, 100),
                    "Fill": np.random.randint(50, 100),
                }
            },
        }

        data.append(data_point)
    
    return tuple(data)

# Data on the effect of each process (?) on the measured variables.
generated_data: tuple
generated_data = generate_random_data(25)

def graph_category(category: str, data: tuple = generated_data) -> None:
    """
    Generates a Graph Based on the Category Given
    
    category:
        the category you want graphed
    """
    # calculates the number of mappings and determine number of plots needed
    number_of_mappings = len(data)
    mappings_per_side = ceil(number_of_mappings ** (1/2))
    # creates the figure and the subplots
    fig, subplots = plt.subplots(ceil(number_of_mappings / mappings_per_side), mappings_per_side)

    for i in range(len(data)):
        subplot = subplots[i // mappings_per_side, i % mappings_per_side]
        mapping_data = data[i]
        # Calculates the amount of bars you need. Assumes all components have even data for all categories.
        category_size = len(mapping_data[tuple(mapping_data.keys())[0]][category]) # accesses first component in memory, then checks the number of elements describing that category in component.
        index = np.arange(category_size) # a list representing all the elements in the category.

        # the dictionary storing the bar contribution for each component
        plots = dict()
        # the bottom of where the bar contribution should be, so that it starts when the last contribution stops
        bottom_val = np.array([0] * category_size)

        # accesses all the metrics data for each component
        components: str
        metric_data: dict
        for (component, metric_data) in mapping_data.items():
            #Creates the plots for each component
            plots[component] = subplot.bar(index, tuple(metric_data[category].values()), width, bottom = bottom_val)
            bottom_val += np.array(tuple(metric_data[category].values()))
        
        # Show title tick marks
        subplot.set_title(f"Mapping {i + 1}")
        subplot.set_ylabel(category)
        subplot.set_xticks(index, tuple(mapping_data[tuple(mapping_data.keys())[0]][category].keys()))
        subplot.set_yticks(np.arange(0, 300, 10))
        subplot.legend(tuple([plot[0] for plot in plots.values()]), tuple(mapping_data.keys()))

    fig.suptitle("Relation of Structure to " + category)

graph_category("Capacity")
graph_category("Access Count")
plt.show()