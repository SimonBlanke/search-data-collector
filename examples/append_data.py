import numpy as np
from hyperactive import Hyperactive
from search_data_collector import CsvSearchData

collector = CsvSearchData("./search_data.csv")  # the csv is created automatically


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
