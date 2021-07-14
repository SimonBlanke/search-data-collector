import time
import numpy as np
import pandas as pd
from hyperactive import Hyperactive

from hyperactive_data_collector import SqlDataCollector


def objective_function(para):
    score = -para["x1"] * para["x1"]
    return score


search_space = {
    "x1": np.arange(0, 1000, 0.1),
}


def search_data_equal(search_data1, search_data2):
    scores1 = search_data1["score"].values
    scores2 = search_data2["score"].values

    assert abs(np.sum(scores1) - np.sum(scores2)) < 0.001


def test_csv_0():
    collector = SqlDataCollector("sqlite:///search_data.db")

    hyper = Hyperactive(verbosity=False)
    hyper.add_search(objective_function, search_space, n_iter=100)
    hyper.run()

    search_data1 = hyper.results(objective_function)

    collector.save(search_data1)
    search_data2 = collector.load()

    search_data_equal(search_data1, search_data2)


def test_csv_1():
    collector = SqlDataCollector("sqlite:///search_data.db")

    hyper = Hyperactive(verbosity=False)
    hyper.add_search(objective_function, search_space, n_iter=100, n_jobs=2)
    hyper.run()

    search_data1 = hyper.results(objective_function)

    collector.save(search_data1)
    search_data2 = collector.load()

    search_data_equal(search_data1, search_data2)


def test_csv_2():
    collector = SqlDataCollector("sqlite:///search_data.db")

    hyper = Hyperactive(verbosity=False)
    hyper.add_search(objective_function, search_space, n_iter=100, n_jobs=-1)
    hyper.run()

    search_data1 = hyper.results(objective_function)

    collector.save(search_data1)
    search_data2 = collector.load()

    search_data_equal(search_data1, search_data2)


collector = SqlDataCollector("sqlite:///search_data.db")


def objective_function_append(para):
    score = -para["x1"] * para["x1"]

    para_dict = para.para_dict
    para_dict["score"] = score
    collector.append(para_dict)

    return score


search_space = {
    "x1": np.arange(0, 1000, 0.1),
}


def test_csv_3():
    hyper = Hyperactive(verbosity=False)
    hyper.add_search(objective_function_append, search_space, n_iter=100)
    hyper.run()

    search_data1 = hyper.results(objective_function_append)

    collector.save(search_data1)
    search_data2 = collector.load()

    search_data_equal(search_data1, search_data2)


collector = SqlDataCollector("sqlite:///search_data.db")


def test_csv_4():
    hyper = Hyperactive(verbosity=False)
    hyper.add_search(objective_function_append, search_space, n_iter=100, n_jobs=4)
    hyper.run()

    search_data1 = hyper.results(objective_function_append)

    collector.save(search_data1)
    search_data2 = collector.load()

    search_data_equal(search_data1, search_data2)


def test_csv_5():
    hyper = Hyperactive(verbosity=False)
    hyper.add_search(objective_function_append, search_space, n_iter=100, n_jobs=-1)
    hyper.run()

    search_data1 = hyper.results(objective_function_append)

    collector.save(search_data1)
    search_data2 = collector.load()

    search_data_equal(search_data1, search_data2)
