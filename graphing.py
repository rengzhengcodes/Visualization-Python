import matplotlib.pyplot as plt
import numpy as np

#np.random.seed(42)

# display conditions
width = 1

#Data Contribution of Each Process
categories = ("DRAM", "DRAM_access_cycles", "PE_cache_space")
data = {
    'M': {
        "DRAM": np.random.randint(50, 100),
        "DRAM_access_cycles": np.random.randint(50, 100),
        "PE_cache_space": np.random.randint(50, 100)
    },
    'N': {
        "DRAM": np.random.randint(50, 100),
        "DRAM_access_cycles": np.random.randint(50, 100),
        "PE_cache_space": np.random.randint(50, 100)
    },
    'K': {
        "DRAM": np.random.randint(50, 100),
        "DRAM_access_cycles": np.random.randint(50, 100),
        "PE_cache_space": np.random.randint(50, 100)
    }
}
print(data)
ind = np.arange(len(categories))

fig = plt.subplots(figsize = (10, 7))
plots = dict()
bottom_val = np.array([0] * 3)

for (key, value) in data.items():
    plots[key] = plt.bar(ind, tuple(value.values()), width, bottom = bottom_val)
    bottom_val = np.array(tuple(value.values())) + bottom_val

plt.title("Relation of Structure to Performance")
plt.ylabel("Contribution of Components")
plt.xticks(ind, categories)
plt.yticks(np.arange(0, 300, 10))
plt.legend(tuple([plot[0] for plot in plots.values()]), tuple(data.keys()))

plt.show()