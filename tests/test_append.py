import time
import pytest
import numpy as np
import pandas as pd
from hyperactive import Hyperactive

from simple_data_collector import DataCollector

from ._test_utils import search_data_equal
from ._search_space_list import search_space_setup

search_space_list = search_space_setup()


@pytest.mark.parametrize("search_space", search_space_list)
def test_append_0(search_space):
    collector = DataCollector("./search_data.csv")
    collector.remove()

    def objective_function(para):
        score = -para["x1"] * para["x1"]

        para_dict = para.para_dict
        para_dict["score"] = score
        collector.append(para_dict)
        return score

    hyper = Hyperactive()
    hyper.add_search(objective_function, search_space, n_iter=15, memory=False)
    hyper.run()

    search_data2 = hyper.search_data(objective_function)
    search_data1 = collector.load(search_space)

    assert search_data_equal(search_data1, search_data2)


@pytest.mark.parametrize("search_space", search_space_list)
def test_append_1(search_space):
    collector = DataCollector("./search_data.csv")
    collector.remove()

    def objective_function(para):
        score = -para["x1"] * para["x1"]

        para_dict = para.para_dict
        para_dict["score"] = score
        collector.append(para_dict)
        return score

    hyper = Hyperactive()
    hyper.add_search(objective_function, search_space, n_iter=15, memory=False)
    hyper.run()

    search_data2 = hyper.search_data(objective_function)
    search_data1 = collector.load()
    search_data1 = collector.conv.str2func(search_data1, search_space)

    assert search_data_equal(search_data1, search_data2)


search_space_list = search_space_setup(search_space_types="functions")


@pytest.mark.parametrize("search_space", search_space_list)
def test_append_2(search_space):
    collector = DataCollector("./search_data.csv")
    collector.remove()

    def objective_function(para):
        score = -para["x1"] * para["x1"]

        para_dict = para.para_dict
        para_dict["score"] = score
        collector.append(para_dict)
        return score

    hyper = Hyperactive()
    hyper.add_search(objective_function, search_space, n_iter=15, memory=False)
    hyper.run()

    search_data2 = hyper.search_data(objective_function)
    search_data1 = collector.load()

    assert not search_data_equal(search_data1, search_data2)


search_space_list = search_space_setup(search_space_types="numeric")


@pytest.mark.parametrize("search_space", search_space_list)
def test_append_3(search_space):
    collector = DataCollector("./search_data.csv")
    collector.remove()

    def objective_function(para):
        score = -para["x1"] * para["x1"]

        para_dict = para.para_dict
        para_dict["score"] = score
        collector.append(para_dict)
        return score

    hyper = Hyperactive()
    hyper.add_search(objective_function, search_space, n_iter=15, memory=False)
    hyper.run()

    search_data2 = hyper.search_data(objective_function)
    search_data1 = collector.load()

    assert search_data_equal(search_data1, search_data2)


@pytest.mark.parametrize("search_space", search_space_list)
def test_append_4(search_space):
    collector = DataCollector("./search_data.csv")
    collector.remove()

    def objective_function(para):
        score = -para["x1"] * para["x1"]

        para_dict = para.para_dict
        para_dict["score"] = score
        collector.append(para_dict)
        return score

    hyper = Hyperactive()
    hyper.add_search(objective_function, search_space, n_iter=15, memory=False)
    hyper.run()

    _search_space_ = {
        "x0": list(np.arange(0, 10)),
        "x1": list(np.arange(0, 10)),
    }

    collector = DataCollector("./search_data.csv")
    hyper = Hyperactive()
    hyper.add_search(objective_function, _search_space_, n_iter=15)
    with pytest.raises(Exception):
        hyper.run()
