from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any


class DataframeReader(metaclass=ABCMeta):
    """
    Dataframe reader abstract class.
    """

    @staticmethod
    @abstractmethod
    def read_df(path: str, extension: str, **kwargs) -> Any:
        """
        Read DataFrame from path.
        """

    @staticmethod
    @abstractmethod
    def write_parquet(df: Any, *args, **kwargs) -> str:
        """
        Write DataFrame as parquet or csv.
        """

    @staticmethod
    @abstractmethod
    def write_table(df: Any, *args, **kwargs) -> str:
        """
        Write DataFrame as table.
        """
