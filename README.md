<H1 align="center">
    Simple Data Collector
</H1>


<p align="center">
  <a href="https://github.com/SimonBlanke/simple-data-collector/actions">
    <img src="https://github.com/SimonBlanke/simple-data-collector/actions/workflows/tests.yml/badge.svg?branch=main" alt="img not loaded: try F5 :)">
  </a>
  <a href="https://app.codecov.io/gh/SimonBlanke/simple-data-collector">
    <img src="https://img.shields.io/codecov/c/github/SimonBlanke/simple-data-collector/main&logo=codecov" alt="img not loaded: try F5 :)">
  </a>
</p>


<H2 align="center">
    Thread-safe and atomic collection of tabular data into csv-files.
</H2>

<br>

The simple-data-collector provides a single class with with following methods:
 - save
 - append
 - load
 - remove

It was created as a utility function for the [Hyperactive-package](https://github.com/SimonBlanke/Hyperactive). It was intended to be used as a search-data collection tool. The search-data can be collected during the optimization run as a dictionary via `append` or after the run as a dataframe with the `save`-method. <br>
The `append`-method is thread-safe to work with hyperactive-multiprocessing. The `save`-method is atomic to avoid accidental data-loss. <br>
The simple-data-collector handles functions in the data by converting them to strings. If the data is loaded you can pass the search_space to convert the strings back to functions.


<br>

## Installation

```console
pip install simple-data-collector 
```


<br>

## Example

```python
import numpy as np
from hyperactive import Hyperactive
from simple_data_collector import DataCollector

collector = DataCollector("./search_data.csv") # the csv is created automatically


def ackley_function(para):
    x, y = para["x"], para["y"]

    loss = (
        -20 * np.exp(-0.2 * np.sqrt(0.5 * (x * x + y * y)))
        - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
        + np.exp(1)
        + 20
    )

    data_dict = para.para_dict
    data_dict["score"] = -loss
    collector.append(data_dict)  # you can append a dictionary to the csv

    return -loss


search_space = {
    "x": list(np.arange(-10, 10, 0.01)),
    "y": list(np.arange(-10, 10, 0.01)),
}


hyper = Hyperactive()
hyper.add_search(ackley_function, search_space, n_iter=3000)
hyper.run()
search_data = hyper.search_data(ackley_function)

# collector.save(search_data) # save a dataframe instead of appending a dictionary

search_data_l = collector.load(search_space)  # load data

print(search_data_l)
```
