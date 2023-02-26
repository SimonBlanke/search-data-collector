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
