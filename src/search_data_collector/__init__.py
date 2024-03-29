# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import importlib.metadata

__version__ = importlib.metadata.version("search-data-collector")
__license__ = "MIT"


from .search_data_collector import SearchDataCollector
from .sql_data_collector import SqlDataCollector

__all__ = ["SearchDataCollector", "SqlDataCollector"]
