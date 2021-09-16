# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numbers


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
    def __init__(self, search_space):
        self.search_space = search_space
        self.data_types = init_data_types(search_space)

    def str2func(self, search_data):
        for para_name in self.data_types.keys():
            data_type = self.data_types[para_name]

            if data_type != "function":
                continue

            func_replace = {}
            for func in self.search_space[para_name]:
                func_name = func.__name__
                func_replace[func_name] = func

            search_data[para_name].replace(func_replace, inplace=True)

        return search_data

    def func2str(self, search_data):
        for para_name in self.data_types.keys():
            data_type = self.data_types[para_name]

            if data_type != "function":
                continue

            func_replace = {}
            for func in self.search_space[para_name]:
                func_name = func.__name__
                func_replace[func] = func_name

            search_data[para_name].replace(func_replace, inplace=True)

        return search_data
