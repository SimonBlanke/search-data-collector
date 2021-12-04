# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import os
import contextlib
import pandas as pd
from filelock import FileLock
from sqlalchemy import create_engine

from .search_data_converter import SearchDataConverter


class DataIO:
    def __init__(self, path):
        self.path = path
        self.replace_existing = False

    def _save_dataframe(self, dataframe, io_wrap):
        dataframe.to_csv(io_wrap, index=False, header=not io_wrap.tell())

    @contextlib.contextmanager
    def atomic_overwrite(self, filename, mode):
        # from: https://stackoverflow.com/questions/42409707/pandas-to-csv-overwriting-prevent-data-loss
        temp = filename + "~"
        with open(temp, mode) as f:
            yield f
        os.rename(temp, filename)  # this will only happen if no exception was raised

    def atomic_write(self, dataframe, path, mode):
        with self.atomic_overwrite(path, mode) as io_wrap:
            self._save_dataframe(dataframe, io_wrap)

    def locked_write(self, dataframe, path):
        lock = FileLock(path + ".lock~")
        with lock:
            with open(path, "a") as io_wrap:
                self._save_dataframe(dataframe, io_wrap)

    def load(self):
        if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
            return pd.read_csv(self.path)


def func2str(obj):
    try:  # is obj
        return obj.__name__
    except:  # is str
        return obj


def df_obj2df_str(df):
    df_obj = df.select_dtypes("object")
    obj_cols = list(df_obj.columns)  # str and obj

    for obj_col in obj_cols:
        df[obj_col] = df[obj_col].apply(func2str)
    return df


class DataSaver:
    def __init__(self, path):
        self.path = path
        self.io = DataIO(path, False)

    def append(self, dictionary):
        dataframe = pd.DataFrame(dictionary, index=[0])
        dataframe = df_obj2df_str(dataframe)
        self.io.locked_write(dataframe, self.path)


class DataCollector:
    def __init__(self, path):
        self.path = path

        self.path2file = path.rsplit("/", 1)[0] + "/"
        self.file_name = path.rsplit("/", 1)[1]

        self.io = DataIO(path)
        self.conv = SearchDataConverter()

    def load(self, search_space=None):
        df = self.io.load()

        if search_space is None:
            return df
        elif isinstance(search_space, dict):
            return self.conv.str2func(df, search_space)
        else:
            print("\n Error")

    def check_conv(self, df):
        if self.conv.data_types is None:
            print("\n check_conv")
            self.conv.dim_types(df)
            print(self.conv.data_types)

    def append(self, dictionary):
        df = pd.DataFrame(dictionary, index=[0])
        self.check_conv(df)

        df = self.conv.func2str(df)
        self.io.locked_write(df, self.path)

    def save(self, df, mode="w"):
        self.check_conv(df)

        df = self.conv.func2str(df)
        self.io.atomic_write(df, self.path, mode)

    def remove(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        if os.path.exists(self.path + ".lock~"):
            os.remove(self.path + ".lock~")
