# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import numbers
import numpy as np


def init_data_types(search_space):
    data_types = {}
    for para_name in search_space.keys():
        value0 = search_space[para_name][0]

        if isinstance(value0, numbers.Number):
            type0 = "number"
            search_dim_ltm = search_space[para_name]

        elif isinstance(value0, str):
            type0 = "string"
            search_dim_ltm = search_space[para_name]

        elif callable(value0):
            type0 = "function"

            search_dim_ltm = []
            for func in list(search_space[para_name]):
                search_dim_ltm.append(func.__name__)
        else:
            type0 = None
            search_dim_ltm = search_space[para_name]
            print("Warning! data type of ", para_name, " not recognized")
            print("Memory will not work")

        data_types[para_name] = type0

    return data_types


class SearchDataConverter:
    def __init__(self):
        self.data_types = None

    def dim_types(self, search_data):
        cols = list(search_data.columns)
        data_types = {}
        for col in cols:
            dim_values = search_data[col].values

            try:
                np.subtract(dim_values, dim_values)
                np.array(dim_values).searchsorted(dim_values)
            except:
                _type_ = "object"
            else:
                _type_ = "number"

            data_types[col] = _type_
        self.data_types = data_types

    def str2func(self, search_data, search_space):
        for para_name in self.data_types.keys():
            data_type = self.data_types[para_name]

            if data_type != "object":
                continue

            func_replace = {}
            for obj_ in search_space[para_name]:
                try:
                    obj_.__name__
                except:
                    func_name = obj_
                else:
                    func_name = obj_.__name__

                func_replace[func_name] = obj_

            if para_name not in list(search_data.columns):
                err = (
                    " Error: parameters of "
                    "search space and previously saved "
                    "search data does not match!"
                )
                print("\n" + err + "\n")

            search_data[para_name].replace(func_replace, inplace=True)

        return search_data

    def func2str(self, search_data):
        for para_name in self.data_types.keys():
            data_type = self.data_types[para_name]

            if data_type != "object":
                continue

            obj_l = list(search_data[para_name].values)

            func_replace = {}
            for obj_ in obj_l:
                try:
                    obj_.__name__
                except:
                    func_name = obj_
                else:
                    func_name = obj_.__name__

                func_replace[obj_] = func_name

            search_data[para_name].replace(func_replace, inplace=True)

        return search_data
