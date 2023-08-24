"""
S3Store module.
"""
from __future__ import annotations

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from sdk.store.objects.base import Store
from sdk.utils.exceptions import StoreError
from sdk.utils.uri_utils import get_uri_netloc


class SqlStore(Store):
    """
    SQL store class. It implements the Store interface and provides methods to fetch and persist
    artifacts on SQL based storage.
    """

    ############################
    # IO methods
    ############################

    def download(self, src: str, dst: str | None = None) -> str:
        """
        Download an artifact from SQL based storage.

        See Also
        --------
        fetch_artifact
        """
        return self._registry.get(src, self.fetch_artifact(src, dst))

    def fetch_artifact(self, src: str, dst: str | None = None) -> str:
        """
        Fetch an artifact from SQL based storage. If the destination is not provided,
        a temporary directory will be created and the artifact will be saved there.

        Parameters
        ----------
        src : str
            Table name.
        dst : str
            The destination of the artifact on local filesystem.

        Returns
        -------
        str
            Returns a file path.
        """
        dst = dst if dst is not None else self._build_temp(src)
        return self._download_table(src, dst)

    def upload(self, src: str, dst: str | None = None) -> str:
        """
        Method to upload an artifact to the backend. Please note that this method is not implemented
        since the SQL store is not meant to upload artifacts.

        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError("SQL store does not support upload.")

    def persist_artifact(self, src: str, dst: str | None = None) -> str:
        """
        Method to persist an artifact. Note that this method is not implemented
        since the SQL store is not meant to write artifacts.

        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError("SQL store does not support persist_artifact.")

    def write_df(self, df: pd.DataFrame, dst: str | None = None, **kwargs) -> str:
        """
        Write a dataframe to a database. Kwargs are passed to df.to_sql().

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe.
        dst : str
            The destination table on database.
        **kwargs
            Keyword arguments.

        Returns
        -------
        str
            The SQL uri where the dataframe was saved.
        """
        if dst is None:
            raise StoreError("Destination table name not provided.")
        return self._upload_table(df, dst, **kwargs)

    ############################
    # Private helper methods
    ############################

    def _get_engine(self) -> Engine:
        """
        Create engine from connection string.

        Returns
        -------
        Engine
            An SQLAlchemy engine.
        """
        connection_string = self.config.get("connection_string")
        if not isinstance(connection_string, str):
            raise StoreError("Connection string must be a string.")
        try:
            return create_engine(connection_string, future=True)
        except Exception as ex:
            raise StoreError(
                f"Something wrong with connection string. Arguments: {str(ex.args)}"
            )

    def _get_schema(self) -> str:
        """
        Get the name of the SQL schema from the URI.

        Returns
        -------
        str
            The name of the SQL schema.
        """
        return get_uri_netloc(self.uri)

    def _check_factory(self) -> tuple[Engine, str]:
        """
        Check if the database is accessible and return the engine and the schema.

        Returns
        -------
        tuple[Engine, str]
            A tuple containing the engine and the schema.
        """
        engine = self._get_engine()
        schema = self._get_schema()
        self._check_access_to_storage(engine)
        return engine, schema

    @staticmethod
    def _check_access_to_storage(engine: Engine) -> None:
        """
        Check if there is access to the storage.

        Parameters
        ----------
        engine : Engine
            An SQLAlchemy engine.

        Returns
        -------
        None

        Raises
        ------
        StoreError
            If there is no access to the storage.
        """
        try:
            engine.connect()
        except SQLAlchemyError:
            engine.dispose()
            raise StoreError("No access to db!")

    def _download_table(self, table: str, dst: str) -> str:
        """
        Download a table from SQL based storage.

        Parameters
        ----------
        table : str
            The source table name.
        dst : str
            The destination path.

        Returns
        -------
        str
            The destination path.
        """
        engine, schema = self._check_factory()
        self._check_local_dst(dst)
        pd.read_sql_table(table, engine, schema=schema).to_parquet(dst, index=False)
        engine.dispose()
        return dst

    def _upload_table(self, df: pd.DataFrame, table: str, **kwargs) -> str:
        """
        Upload a table to SQL based storage.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe.
        table : str
            The destination table name.
        **kwargs
            Keyword arguments.

        Returns
        -------
        str
            The SQL URI where the dataframe was saved.
        """
        engine, schema = self._check_factory()
        df.to_sql(table, engine, schema=schema, index=False, **kwargs)
        engine.dispose()
        return f"sql://{schema}.{table}"

    ############################
    # Store interface methods
    ############################

    def _validate_uri(self) -> None:
        """
        Validate the URI of the store.

        Returns
        -------
        None

        Raises
        ------
        StoreError
            If the URI scheme is not 'sql'.

        StoreError
            If no schema is specified in the URI.
        """
        super()._validate_uri()
        if self._get_schema() == "":
            raise StoreError("No schema specified in the URI for sql store!")

    @staticmethod
    def is_local() -> bool:
        """
        Check if the store is local.

        Returns
        -------
        bool
            False
        """
        return False
