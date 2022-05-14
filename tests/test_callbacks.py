import os
import time
import random
import pytest
import numpy as np
import pandas as pd
from hyperactive import Hyperactive

from simple_data_collector import DataCollector

from ._test_utils import search_data_equal

############################## create search spaces
size = 1000

dim_full = list(range(0, size))
dim_cat = list(range(round(size / 3)))
dim_10 = list(range(round(size ** 0.1)))

search_space_0 = {
    "x1": dim_full,
}

search_space_1 = {
    "x1": dim_cat,
    "x2": list(range(3)),
}

search_space_2 = {
    "x1": dim_10,
    "x2": dim_10,
    "x3": dim_10,
    "x4": dim_10,
    "x5": dim_10,
    "x6": dim_10,
    "x7": dim_10,
    "x8": dim_10,
    "x9": dim_10,
    "x10": dim_10,
}

search_space_3 = {
    "x1": dim_10,
    "x2": dim_10,
    "x3": dim_10,
    "x4": dim_10,
    "x5": dim_10,
    "x6": dim_10,
    "x7": dim_10,
    "x8": dim_10,
    "x9": dim_10,
    "x10": dim_10,
    "x11": [1],
    "x12": [1],
    "x13": [1],
    "x14": [1],
    "x15": [1],
}

search_space_4 = {
    "x1": dim_cat,
    "str1": ["0", "1", "2"],
}


def func1():
    pass


def func2():
    pass


def func3():
    pass


search_space_5 = {
    "x1": dim_cat,
    "func1": [func1, func2, func3],
}


class class1:
    pass


class class2:
    pass


class class3:
    pass


def wr_func_1():
    return class1


def wr_func_2():
    return class2


def wr_func_3():
    return class3


search_space_6 = {
    "x1": dim_cat,
    "class_1": [wr_func_1, wr_func_2, wr_func_3],
}


class class1_o:
    def __init__(self):
        pass


class class2_o:
    def __init__(self):
        pass


class class3_o:
    def __init__(self):
        pass


def wr_func_1():
    return class1_o()


def wr_func_2():
    return class2_o()


def wr_func_3():
    return class3_o()


search_space_7 = {
    "x1": dim_cat,
    "class_obj_1": [wr_func_1, wr_func_2, wr_func_3],
}


def wr_func_1():
    return [1, 0, 0]


def wr_func_2():
    return [0, 1, 0]


def wr_func_3():
    return [0, 0, 1]


search_space_8 = {
    "x1": dim_cat,
    "list_1": [wr_func_1, wr_func_2, wr_func_3],
}


def wr_func_1():
    return np.array([1, 0, 0])


def wr_func_2():
    return np.array([0, 1, 0])


def wr_func_3():
    return np.array([0, 0, 1])


search_space_9 = {
    "x1": dim_cat,
    "array_1": [wr_func_1, wr_func_2, wr_func_3],
}


def wr_func_1():
    return pd.DataFrame(np.array([1, 0, 0]))


def wr_func_2():
    return pd.DataFrame(np.array([0, 1, 0]))


def wr_func_3():
    return pd.DataFrame(np.array([0, 0, 1]))


search_space_10 = {
    "x1": dim_cat,
    "df_1": [wr_func_1, wr_func_2, wr_func_3],
}

search_space_list = [
    (search_space_0),
    (search_space_1),
    (search_space_2),
    (search_space_3),
    (search_space_4),
    (search_space_5),
    (search_space_6),
    (search_space_7),
    (search_space_8),
    (search_space_9),
    (search_space_10),
]

############################## start tests


@pytest.mark.parametrize("search_space", search_space_list)
def test_append_0(search_space):
    collector = DataCollector("./search_data.csv")
    collector.remove()

    def callback1(path):
        if os.path.isfile(path) and os.path.getsize(path) > 0:
            dataframe = pd.read_csv(path).head(10)

            rnd = int(random.randint(0, 9) / 100)
            time.sleep(rnd)

            os.remove(path)

            rnd = int(random.randint(0, 9) / 100)
            time.sleep(rnd)

            with open(path, "a") as io_wrap:
                dataframe.to_csv(io_wrap, index=False, header=not io_wrap.tell())

    def objective_function(para):
        score = -para["x1"] * para["x1"]

        para_dict = para.para_dict
        para_dict["score"] = score
        collector.append(para_dict, callbacks={"before": [callback1]})
        return score

    hyper = Hyperactive(distribution="pathos")
    hyper.add_search(
        objective_function, search_space, n_iter=100, n_jobs=4, memory=False
    )
    hyper.run()


@pytest.mark.parametrize("search_space", search_space_list)
def test_append_1(search_space):
    collector = DataCollector("./search_data.csv")
    collector.remove()

    def callback1(path):
        if os.path.isfile(path) and os.path.getsize(path) > 0:
            dataframe = pd.read_csv(path).head(10)

            rnd = int(random.randint(0, 9) / 100)
            time.sleep(rnd)

            os.remove(path)

            rnd = int(random.randint(0, 9) / 100)
            time.sleep(rnd)

            with open(path, "a") as io_wrap:
                dataframe.to_csv(io_wrap, index=False, header=not io_wrap.tell())

    def objective_function(para):
        score = -para["x1"] * para["x1"]

        para_dict = para.para_dict
        para_dict["score"] = score
        collector.append(para_dict, callbacks={"after": [callback1]})
        return score

    hyper = Hyperactive(distribution="pathos")
    hyper.add_search(
        objective_function, search_space, n_iter=100, n_jobs=4, memory=False
    )
    hyper.run()
