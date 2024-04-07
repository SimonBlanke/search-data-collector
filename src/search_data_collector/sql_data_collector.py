import sqlalchemy as sql

import os
import pandas as pd

from .search_data_converter import SearchDataConverter


class SqlSearchData:
    def __init__(self, path, func2str=True) -> None:
        self.path = path
        self.func2str = func2str

        self.ml_data_path = "sqlite:///" + path
        self.conv = SearchDataConverter()

        self.dbEngine = sql.create_engine(self.ml_data_path)

    def load(self, table, search_space=None):
        if not os.path.isfile(self.path):
            msg = "SQL Database does not exist in path: " + self.path
            raise FileNotFoundError(msg)

        df = pd.read_sql_table(table, self.dbEngine)
        if search_space is None:
            return df
        elif isinstance(search_space, dict):
            return self.conv.str2func(df, search_space)
        else:
            raise ValueError

    def append(self, table, dictionary):
        dataframe = pd.DataFrame(dictionary, index=[0])

        if self.func2str:
            dataframe = self.conv.func2str(dataframe)

        dataframe.to_sql(name=table, con=self.dbEngine, index=False, if_exists="append")

    def save(self, table, dataframe, if_exists="replace"):
        if self.func2str:
            ft_tmp = dataframe.copy()
            dataframe = self.conv.func2str(ft_tmp)

        dataframe.to_sql(
            name=table, con=self.dbEngine, index=False, if_exists=if_exists
        )

    def remove(self, table):
        try:
            tbl = sql.Table(table, sql.MetaData(), autoload_with=self.dbEngine)
            tbl.drop(self.dbEngine, checkfirst=False)
        except sql.exc.NoSuchTableError as e:
            pass

    @property
    def tables(self):
        return self.dbEngine.table_names()
