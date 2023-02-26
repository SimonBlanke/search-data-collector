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
