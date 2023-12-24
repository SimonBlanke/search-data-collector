import time
import pytest
import numpy as np
import pandas as pd
from hyperactive import Hyperactive

from search_data_collector import SqlDataCollector

from .._test_utils import search_data_equal
from .._search_space_list import search_space_setup

search_space_list = search_space_setup()
table = "test_table"


def objective_function(para):
    score = -para["x1"] * para["x1"]
    return score


search_space = {
    "x1": list(np.arange(0, 1000, 0.1)),
}


def objective_function(para):
    score = -para["x1"] * para["x1"]
    return score


objective_para = (
    "objective",
    [
        (objective_function),
    ],
)

path = "./search_data.db"


@pytest.mark.parametrize("search_space", search_space_list)
@pytest.mark.parametrize(*objective_para)
def test_hyperactive_save_0(objective, search_space):
    print("\n search_space \n", search_space)

    collector = SqlDataCollector(path)
    collector.remove(table)

    hyper = Hyperactive()
    hyper.add_search(objective, search_space, n_iter=15)
    hyper.run()

    search_data2 = hyper.search_data(objective)
    collector.save(table, search_data2)
    search_data1 = collector.load(table, search_space)

    assert search_data_equal(search_data1, search_data2)


@pytest.mark.parametrize("search_space", search_space_list)
@pytest.mark.parametrize(*objective_para)
def test_hyperactive_save_1(objective, search_space):
    print("\n search_space \n", search_space)

    collector = SqlDataCollector(path)
    collector.remove(table)

    hyper = Hyperactive()
    hyper.add_search(objective, search_space, n_iter=15)
    hyper.run()

    search_data2 = hyper.search_data(objective)
    collector.save(table, search_data2)
    search_data1 = collector.load(table)
    search_data1 = collector.conv.str2func(search_data1, search_space)

    assert search_data_equal(search_data1, search_data2)


search_space_list = search_space_setup(search_space_types="numeric")


@pytest.mark.parametrize("search_space", search_space_list)
@pytest.mark.parametrize(*objective_para)
def test_hyperactive_save_3(objective, search_space):
    print("\n search_space \n", search_space)

    collector = SqlDataCollector(path)
    collector.remove(table)

    hyper = Hyperactive()
    hyper.add_search(objective, search_space, n_iter=15)
    hyper.run()

    search_data2 = hyper.search_data(objective)
    collector.save(table, search_data2)
    search_data1 = collector.load(table)

    assert search_data_equal(search_data1, search_data2)
