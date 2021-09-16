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
    def __init__(self, path, drop_duplicates):
        self.path = path
        self.replace_existing = False
        self.drop_duplicates = drop_duplicates

    def _save_dataframe(self, dataframe, io_wrap):
        if self.drop_duplicates:
            dataframe.drop_duplicates(subset=self.drop_duplicates, inplace=True)

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

    def load(self, path):
        if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
            return pd.read_csv(self.path)


def func2str(obj):
    try:
        return obj.__name__
    except:
        return obj


def df_obj2df_str(df):
    df_obj = df.select_dtypes("object")
    obj_cols = list(df_obj.columns)

    for col in list(df_obj.columns):
        df_obj[col] = df_obj[col].apply(func2str)

    df[obj_cols] = df_obj

    return df


class DataCollector:
    def __init__(self, path, search_space=None, drop_duplicates=False):
        self.path = path
        self.search_space = search_space
        self.drop_duplicates = drop_duplicates

        self.path2file = path.rsplit("/", 1)[0] + "/"
        self.file_name = path.rsplit("/", 1)[1]

        self.io = DataIO(path, drop_duplicates)

        if search_space is None:
            self.func2str = df_obj2df_str
        elif isinstance(search_space, dict):
            self.conv = SearchDataConverter(search_space)
            self.func2str = self.conv.func2str
        else:
            print("Error")

    def load(self):
        if self.search_space is None:
            print("Error")
        elif isinstance(self.search_space, dict):
            df = self.io.load(self.path)
            if df is not None:
                return self.conv.str2func(df)
        else:
            print("Error")

    def append(self, dictionary):
        dataframe = pd.DataFrame(dictionary, index=[0])
        dataframe = self.func2str(dataframe)
        self.io.locked_write(dataframe, self.path)

    def save(self, dataframe, mode="w"):
        dataframe = self.func2str(dataframe)
        self.io.atomic_write(dataframe, self.path, mode)

    def remove(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        if os.path.exists(self.path + ".lock~"):
            os.remove(self.path + ".lock~")


"""
class SqlStorage:
    def __init__(self, storage, echo=False):
        self.storage = storage
        self.engine = create_engine(storage, echo=echo)

        self.db_path = self.engine.url.database

    def load(self, table="default"):
        return pd.read_sql(table, self.engine)

    def append(self, dictionary, table="default"):
        dataframe = pd.DataFrame(dictionary, index=[0])

        lock = FileLock(self.db_path + ".lock~")
        with lock:
            dataframe.to_sql(table, self.engine, if_exists="append")

    def save(self, dataframe, table="default", if_exists="replace"):
        dataframe.to_sql(table, self.engine, if_exists=if_exists)

    def remove(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.db_path + ".lock~"):
            os.remove(self.db_path + ".lock~")
"""
