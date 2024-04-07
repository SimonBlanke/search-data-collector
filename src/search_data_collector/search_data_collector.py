# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import os
import contextlib
import pandas as pd
from filelock import FileLock

from .search_data_converter import SearchDataConverter


class DataIo:
    def __init__(self, path):
        self.path = path
        self.lock_path = self.path + ".lock~"

        self.replace_existing = False
        self.callbacks = None

    def _save_dataframe(self, dataframe, io_wrap):
        dataframe.to_csv(io_wrap, index=False, header=not io_wrap.tell())

    def _run_callbacks(self, type_):
        if self.callbacks and type_ in self.callbacks:
            [callback(self.path) for callback in self.callbacks[type_]]

    @contextlib.contextmanager
    def atomic_overwrite(self, mode):
        # from: https://stackoverflow.com/questions/42409707/pandas-to-csv-overwriting-prevent-data-loss
        temp = self.path + "~"
        with open(temp, mode) as f:
            yield f
        os.rename(temp, self.path)  # this will only happen if no exception was raised

    def atomic_write(self, dataframe, mode):
        self.check_col_names(dataframe)

        old_df = self.load()
        if isinstance(old_df, pd.DataFrame):
            dataframe = old_df.append(dataframe)

        with self.atomic_overwrite(mode) as io_wrap:
            self._save_dataframe(dataframe, io_wrap)

    def check_col_names(self, dataframe):
        if os.path.exists(self.path) and len(dataframe) > 0:
            csv_col_names = pd.read_csv(self.path, nrows=0).columns.tolist()
            df_col_names = list(dataframe.columns)

            if csv_col_names != df_col_names:
                msg = (
                    "Data header does not match csv header:\n",
                    csv_col_names,
                    "\n",
                    df_col_names,
                )
                raise Exception(msg)

    def locked_write(self, dataframe, callbacks):
        self.callbacks = callbacks

        lock = FileLock(self.lock_path)

        with lock:
            self.check_col_names(dataframe)

            self._run_callbacks("before")
            with open(self.path, "a") as io_wrap:
                self._save_dataframe(dataframe, io_wrap)
            self._run_callbacks("after")

    def remove_lock(self):
        if os.path.isfile(self.lock_path):
            os.remove(self.lock_path)

    def load(self):
        if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
            return pd.read_csv(self.path)


def func2str(obj):
    try:  # is obj
        return obj.__name__
    except:  # is str
        return obj


class CsvSearchData:
    def __init__(self, path, func2str=True):
        self.path = path
        self.func2str = func2str

        self.io = DataIo(path)
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
            raise ValueError

    def append(self, dictionary, callbacks={}):
        dataframe = pd.DataFrame(dictionary, index=[0])
        self.is_df_valid(dataframe)

        if self.func2str:
            dataframe = self.conv.func2str(dataframe)
        self.io.locked_write(dataframe, callbacks)

    def save(self, dataframe, mode="w"):
        self.is_df_valid(dataframe)

        if self.func2str:
            ft_tmp = dataframe.copy()
            dataframe = self.conv.func2str(ft_tmp)
        self.io.atomic_write(dataframe, mode)

    def remove(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        if os.path.exists(self.path + ".lock~"):
            os.remove(self.path + ".lock~")
