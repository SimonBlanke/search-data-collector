import numpy as np
from gradient_free_optimizers import RandomSearchOptimizer
from search_data_collector import CsvSearchData

collector = CsvSearchData("./search_data.csv")  # the csv is created automatically
collector.remove()  # cleanup existing data


def parabola_function(para):
    loss = para["x"] * para["x"] + para["y"] * para["y"]

    data_dict = dict(para)  # copy the parameter dictionary
    data_dict["score"] = -loss  # add the score to the dictionary
    collector.append(data_dict)  # you can append a dictionary to the csv

    return -loss


search_space = {
    "x": np.arange(-10, 10, 0.1),
    "y": np.arange(-10, 10, 0.1),
}


opt = RandomSearchOptimizer(search_space)
opt.search(parabola_function, n_iter=100)
search_data = opt.search_data

search_data = collector.load(search_space)  # load data
print("\n search_data \n", search_data)
