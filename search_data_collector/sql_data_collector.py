import os
import pandas as pd
from filelock import FileLock
from sqlalchemy import create_engine


class SqlDataCollector:
    def __init__(self, storage, echo=False):
        self.storage = storage
        self.engine = create_engine(storage, echo=echo)

        self.db_path = self.engine.url.database

    def load(self, table_name="search_data", search_space=None):
        search_data = pd.read_sql(table_name, self.engine)

        if search_space is None:
            return search_data
        elif isinstance(search_space, dict):
            return self.conv.str2func(search_data, search_space)
        else:
            raise ValueError

    def append(self, dictionary):
        dataframe = pd.DataFrame(dictionary, index=[0])

        lock = FileLock(self.db_path + ".lock~")
        with lock:
            dataframe.to_sql("search_data", self.engine, if_exists="append")

    def save(self, dataframe, table_name="search_data", if_exists="replace"):
        dataframe.to_sql(table_name, self.engine, if_exists=if_exists)

    def remove(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.db_path + ".lock~"):
            os.remove(self.db_path + ".lock~")
