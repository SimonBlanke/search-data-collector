import time
import pytest
import numpy as np
import pandas as pd
from hyperactive import Hyperactive

from simple_data_collector import DataCollector

from ._test_utils import search_data_equal
from ._search_space_list import search_space_setup

search_space_list = search_space_setup()

"""
@pytest.mark.parametrize("search_space", search_space_list)
def test_hyperactive_0(search_space):
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
"""


def test_long_term_memory():
    pass


def test_progress_board():
    pass
