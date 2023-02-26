<H1 align="center">
    Search Data Collector
</H1>


<p align="center">
  <a href="https://github.com/SimonBlanke/search-data-collector/actions">
    <img src="https://github.com/SimonBlanke/search-data-collector/actions/workflows/tests.yml/badge.svg?branch=main" alt="img not loaded: try F5 :)">
  </a>
  <a href="https://app.codecov.io/gh/SimonBlanke/search-data-collector">
    <img src="https://img.shields.io/codecov/c/github/SimonBlanke/search-data-collector/main&logo=codecov" alt="img not loaded: try F5 :)">
  </a>
</p>


<H2 align="center">
    Thread-safe and atomic collection of tabular data into csv-files.
</H2>

<br>

The search-data-collector provides a single class with following methods to manage data:
 - save
 - append
 - load
 - remove

The Search-Data-Collector was created as a utility function for the [Gradient-Free-Optimizers](https://github.com/SimonBlanke/Gradient-Free-Optimizers)- and [Hyperactive](https://github.com/SimonBlanke/Hyperactive)-package. It is intended to be used as a tool to collect search-data from the optimization run. The search-data can be collected during the optimization run as a dictionary via `append` or after the run as a dataframe with the `save`-method. <br>
The `append`-method is thread-safe to work with hyperactive-multiprocessing. The `save`-method is atomic to avoid accidental data-loss, when interupting the save-process. <br>
For the Hyperactive-package the search-data-collector handles functions in the data by converting them to strings. If the data is loaded you can pass the search-space to convert the strings back to functions. 



<br>

## Disclaimer

This project is in an early development stage and is sparsely tested. If you encounter bugs or have suggestions for improvements, then please open an issue.


<br>

## Installation

```console
pip install search-data-collector 
```


<br>

## Examples


<br>

### Append search-data

```python
import numpy as np
from hyperactive import Hyperactive
from search_data_collector import SearchDataCollector

collector = SearchDataCollector("./search_data.csv")  # the csv is created automatically


def parabola_function(para):
    loss = para["x"] * para["x"] + para["y"] * para["y"]

    data_dict = dict(para)  # copy the parameter dictionary
    data_dict["score"] = -loss  # add the score to the dictionary
    collector.append(data_dict)  # you can append a dictionary to the csv

    return -loss


search_space = {
    "x": list(np.arange(-10, 10, 0.1)),
    "y": list(np.arange(-10, 10, 0.1)),
}


hyper = Hyperactive()
hyper.add_search(parabola_function, search_space, n_iter=1000)
hyper.run()
search_data = hyper.search_data(parabola_function)

search_data = collector.load(search_space)  # load data

print("\n search_data \n", search_data)
```


<br>

### Save search-data

```python
import numpy as np
from hyperactive import Hyperactive
from search_data_collector import SearchDataCollector

collector = SearchDataCollector("./search_data.csv")  # the csv is created automatically


def parabola_function(para):
    loss = para["x"] * para["x"] + para["y"] * para["y"]

    return -loss


search_space = {
    "x": list(np.arange(-10, 10, 0.1)),
    "y": list(np.arange(-10, 10, 0.1)),
}


hyper = Hyperactive()
hyper.add_search(parabola_function, search_space, n_iter=1000)
hyper.run()
search_data = hyper.search_data(parabola_function)

collector.save(search_data)  # save a dataframe instead

search_data = collector.load(search_space)  # load data

print("\n search_data \n", search_data)
```



<br>

### Functions in the search-space/search-data

```python
import numpy as np
from hyperactive import Hyperactive
from search_data_collector import SearchDataCollector

collector = SearchDataCollector("./search_data.csv")  # the csv is created automatically


def parabola_function(para):
    loss = para["x"] * para["x"] + para["y"] * para["y"]

    return -loss


# just some dummy functions to show how this works


def function1():
    print("this is function1")


def function2():
    print("this is function2")


def function3():
    print("this is function3")


search_space = {
    "x": list(np.arange(-10, 10, 0.1)),
    "y": list(np.arange(-10, 10, 0.1)),
    "string.example": ["string1", "string2", "string3"],
    "function.example": [function1, function2, function3],
}


hyper = Hyperactive()
hyper.add_search(parabola_function, search_space, n_iter=30)
hyper.run()
search_data = hyper.search_data(parabola_function)

collector.save(search_data)  # save a dataframe instead of appending a dictionary

search_data = collector.load()  # load data

print(
    "\n In this dataframe the 'function.example'-column contains strings, which are the '__name__' of the functions. \n search_data \n ",
    search_data,
    "\n",
)

search_data = collector.load(search_space)  # load data with search-space

print(
    print(
        "\n In this dataframe the 'function.example'-column contains the functions again. \n search_data \n ",
        search_data,
        "\n",
    )
)
```
