# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import os
import contextlib
import pandas as pd
from filelock import FileLock

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
        self.check_col_names(dataframe, path)

        with self.atomic_overwrite(path, mode) as io_wrap:
            self._save_dataframe(dataframe, io_wrap)

    def check_col_names(self, dataframe, path):
        if os.path.exists(path):
            csv_col_names = pd.read_csv(path, nrows=0).columns.tolist()
            df_col_names = list(dataframe.columns)

            if csv_col_names != df_col_names:
                raise Exception("Data header does not match csv header")

    def locked_write(self, dataframe, path):
        lock = FileLock(path + ".lock~")
        with lock:
            self.check_col_names(dataframe, path)
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

    @staticmethod
    def is_df_valid(df):
        if df is None:
            print("Warning: Loaded dataframe is None")
            return False
        elif len(df) == 0:
            print("Warning: Loaded dataframe is empty")
            return False

        return True

    def load(self, search_space=None):
        df = self.io.load()
        if not self.is_df_valid(df):
            return df

        if search_space is None:
            return df
        elif isinstance(search_space, dict):
            return self.conv.str2func(df, search_space)
        else:
            print("\n Error")

    def append(self, dictionary, func2str=True):
        df = pd.DataFrame(dictionary, index=[0])
        self.is_df_valid(df)

        if func2str:
            df = self.conv.func2str(df)
        self.io.locked_write(df, self.path)

    def save(self, df, func2str=True, mode="w"):
        self.is_df_valid(df)

        if func2str:
            ft_tmp = df.copy()
            df = self.conv.func2str(ft_tmp)
        self.io.atomic_write(df, self.path, mode)

    def remove(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        if os.path.exists(self.path + ".lock~"):
            os.remove(self.path + ".lock~")
