import time
import numpy as np
import pandas as pd
from hyperactive import Hyperactive

from hyperactive_data_collector import CsvDataCollector


def objective_function(para):
    score = -para["x1"] * para["x1"]
    return score


search_space = {
    "x1": np.arange(0, 1000, 0.1),
}


def search_data_equal(search_data1, search_data2):
    scores1 = search_data1["score"].values
    scores2 = search_data2["score"].values

    print("\n scores1 \n", scores1, scores1.shape)
    print("\n scores2 \n", scores2, scores2.shape)

    assert abs(np.sum(scores1) - np.sum(scores2)) < 0.001


def test_csv_0():
    collector = CsvDataCollector("./search_data.csv")

    hyper = Hyperactive(verbosity=False)
    hyper.add_search(objective_function, search_space, n_iter=100, memory=False)
    hyper.run()

    search_data1 = hyper.results(objective_function)

    collector.save(search_data1)
    search_data2 = collector.load()
    collector.remove()

    search_data_equal(search_data1, search_data2)


def test_csv_1():
    collector = CsvDataCollector("./search_data.csv")

    hyper = Hyperactive(verbosity=False)
    hyper.add_search(
        objective_function, search_space, n_iter=100, n_jobs=2, memory=False
    )
    hyper.run()

    search_data1 = hyper.results(objective_function)

    collector.save(search_data1)
    search_data2 = collector.load()
    collector.remove()

    search_data_equal(search_data1, search_data2)


def test_csv_2():
    collector = CsvDataCollector("./search_data.csv")

    hyper = Hyperactive(verbosity=False)
    hyper.add_search(
        objective_function, search_space, n_iter=100, n_jobs=-1, memory=False
    )
    hyper.run()

    search_data1 = hyper.results(objective_function)

    collector.save(search_data1)
    search_data2 = collector.load()
    collector.remove()

    search_data_equal(search_data1, search_data2)


collector1 = CsvDataCollector("./search_data1.csv")


def objective_function_append1(para):
    score = -para["x1"] * para["x1"]

    para_dict = para.para_dict
    para_dict["score"] = score
    collector1.append(para_dict)

    return score


def test_csv_3():
    hyper = Hyperactive(verbosity=False)
    hyper.add_search(objective_function_append1, search_space, n_iter=100, memory=False)
    hyper.run()

    search_data1 = hyper.results(objective_function_append1)
    search_data2 = collector1.load()
    collector1.remove()

    search_data_equal(search_data1, search_data2)


collector2 = CsvDataCollector("./search_data2.csv")


def objective_function_append2(para):
    score = -para["x1"] * para["x1"]

    para_dict = para.para_dict
    para_dict["score"] = score
    collector2.append(para_dict)

    return score


def test_csv_4():
    hyper = Hyperactive(verbosity=False)
    hyper.add_search(
        objective_function_append2, search_space, n_iter=100, n_jobs=4, memory=False
    )
    hyper.run()

    search_data1 = hyper.results(objective_function_append2)
    search_data2 = collector2.load()
    collector2.remove()

    search_data_equal(search_data1, search_data2)


collector3 = CsvDataCollector("./search_data3.csv")


def objective_function_append3(para):
    score = -para["x1"] * para["x1"]

    para_dict = para.para_dict
    para_dict["score"] = score
    collector3.append(para_dict)

    return score


def test_csv_5():
    hyper = Hyperactive(verbosity=False)
    hyper.add_search(
        objective_function_append3, search_space, n_iter=100, n_jobs=-1, memory=False
    )
    hyper.run()

    search_data1 = hyper.results(objective_function_append3)
    search_data2 = collector3.load()
    collector3.remove()

    search_data_equal(search_data1, search_data2)
