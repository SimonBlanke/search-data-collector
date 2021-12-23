import time
import pytest
import numpy as np
import pandas as pd
from hyperactive import Hyperactive

from simple_data_collector import DataCollector

from ._test_utils import search_data_equal
from ._search_space_list import search_space_setup

search_space_list = search_space_setup()


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


@pytest.mark.parametrize(*objective_para)
def test_remove_0(objective):
    collector = DataCollector("./search_data")
    collector.remove()

    search_data = collector.load()

    assert search_data is None
