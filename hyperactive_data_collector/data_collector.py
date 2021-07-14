# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import os
import contextlib
import pandas as pd
from filelock import FileLock
from sqlalchemy import create_engine


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


class CsvDataCollector:
    def __init__(self, path, drop_duplicates=False):
        self.path = path
        self.drop_duplicates = drop_duplicates

        self.path2file = path.rsplit("/", 1)[0] + "/"
        self.file_name = path.rsplit("/", 1)[1]

        self.io = DataIO(path, drop_duplicates)

    def load(self):
        return self.io.load(self.path)

    def append(self, dictionary):
        dataframe = pd.DataFrame(dictionary, index=[0])
        self.io.locked_write(dataframe, self.path)

    def save(self, dataframe, mode="w"):
        self.io.atomic_write(dataframe, self.path, mode)


class SqlDataCollector:
    def __init__(self, storage, echo=False):
        self.storage = storage
        self.engine = create_engine(storage, echo=echo)

        self.db_path = self.engine.url.database

    def load(self, table_name="search_data"):
        return pd.read_sql(table_name, self.engine)

    def append(self, dictionary):
        dataframe = pd.DataFrame(dictionary, index=[0])

        lock = FileLock(self.db_path + ".lock~")
        with lock:
            dataframe.to_sql("search_data", self.engine, if_exists="append")

    def save(self, dataframe, table_name="search_data", if_exists="replace"):
        dataframe.to_sql(table_name, self.engine, if_exists=if_exists)
