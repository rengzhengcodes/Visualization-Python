from typing import Union
# defines the numeric data type for type hinting
numeric = Union[float, int]

import matplotlib.pyplot as plt
import numpy as np

#np.random.seed(42)

# display conditions
width = 1

# thing's we're trying to measure generally, versus what we need to map to see them
categories = {
    "Capacity": ["L1", "L2"],
    "Access Count": ["Read", "Write", "Fill"]
}

def generate_random_data(data_points: int) -> list:
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
    
    return data

# Data on the effect of each process (?) on the measured variables.
generated_data = generate_random_data(5)

def graph_category(category: str, data: dict = generated_data[0]) -> None:
    """
    Generates a Graph Based on the Category Given
    
    category:
        the category you want graphed
    """
    # Calculates the amount of bars you need. Assumes all components have even data for all categories.
    category_size = len(data[tuple(data.keys())[0]][category]) # accesses first component in memory, then checks the number of elements describing that category in component.
    index = np.arange(category_size) # a list representing all the elements in the category.

    # defines the figure we're showing 
    fig = plt.subplots(figsize = (10, 7))
    # the dictionary storing the bar contribution for each component
    plots = dict()
    # the bottom of where the bar contribution should be, so that it starts when the last contribution stops
    bottom_val = np.array([0] * category_size)

    # accesses all the metrics data for each component
    components: str
    metric_data: numeric
    for (component, metric_data) in data.items():
        print(tuple(metric_data[category].values()))
        #Creates the plots for each component
        plots[component] = plt.bar(index, tuple(metric_data[category].values()), width, bottom = bottom_val)
        bottom_val += np.array(tuple(metric_data[category].values()))
    
    # Show title tick marks
    plt.title("Relation of Structure to " + category)
    plt.ylabel("Graph of Each Step")
    plt.xticks(index, tuple(data[tuple(data.keys())[0]][category].keys()))
    plt.yticks(np.arange(0, 300, 10))
    plt.legend(tuple([plot[0] for plot in plots.values()]), tuple(data.keys()))

    plt.show()

graph_category("Capacity")