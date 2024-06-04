from __future__ import annotations

from io import BytesIO
from typing import Any

import pandas as pd
from digitalhub_data.readers.objects.base import DataframeReader


class DataframeReaderPandas(DataframeReader):
    """
    Pandas reader class.
    """

    @staticmethod
    def read_df(path: str, extension: str, **kwargs) -> pd.DataFrame:
        """
        Read DataFrame from path.

        Parameters
        ----------
        path : str
            Path to read DataFrame from.
        extension : str
            Extension of the file.
        **kwargs
            Keyword arguments.

        Returns
        -------
        pd.DataFrame
            Pandas DataFrame.
        """
        if extension == "csv":
            return pd.read_csv(path, **kwargs)
        return pd.read_parquet(path, **kwargs)

    def write_df(self, df: pd.DataFrame, dst: str | BytesIO, extension: str | None = None, **kwargs) -> None:
        """
        Write DataFrame as parquet.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to write.
        dst : str | BytesIO
            The destination of the dataframe.
        **kwargs
            Keyword arguments.

        Returns
        -------
        None
        """
        if extension == "csv":
            return self.write_csv(df, dst, **kwargs)
        self.write_parquet(df, dst, **kwargs)

    @staticmethod
    def write_csv(df: pd.DataFrame, dst: str | BytesIO, **kwargs) -> None:
        """
        Write DataFrame as csv.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to write.
        dst : str | BytesIO
            The destination of the dataframe.
        **kwargs
            Keyword arguments.

        Returns
        -------
        None
        """
        df.to_csv(dst, index=False, **kwargs)

    @staticmethod
    def write_parquet(df: pd.DataFrame, dst: str | BytesIO, **kwargs) -> None:
        """
        Write DataFrame as parquet.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to write.
        dst : str | BytesIO
            The destination of the dataframe.
        **kwargs
            Keyword arguments.

        Returns
        -------
        None
        """
        df.to_parquet(dst, index=False, **kwargs)

    @staticmethod
    def write_table(df: pd.DataFrame, table: str, engine: Any, schema: str, **kwargs) -> None:
        """
        Write DataFrame as table.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to write.
        table : str
            The destination table.
        engine : Any
            The SQLAlchemy engine.
        schema : str
            The destination schema.
        **kwargs
            Keyword arguments.

        Returns
        -------
        None
        """
        df.to_sql(table, engine, schema=schema, index=False, **kwargs)
