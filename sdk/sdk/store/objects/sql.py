"""
S3Store module.
"""
from __future__ import annotations

from tempfile import mkdtemp

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from sdk.store.objects.base import Store
from sdk.utils.exceptions import StoreError
from sdk.utils.file_utils import check_make_dir, get_dir
from sdk.utils.uri_utils import get_name_from_uri, get_uri_netloc, get_uri_scheme


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
        return self.fetch_artifact(src, dst)

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
        if dst is None:
            tmpdir = mkdtemp()
            dst = f"{tmpdir}/{get_name_from_uri(src)}"
            self._register_resource(f"{src}", dst)

        # Get engine
        engine = self._get_engine()

        # Check store access
        self._check_access_to_storage(engine)

        # Check if local destination exists
        self._check_local_dst(dst)

        # Get table from db and save it locally
        df = pd.read_sql_table(src, engine)
        df.to_parquet(dst, index=False)

        # Close connection
        engine.dispose()
        return dst

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
        # Get engine
        engine = self._get_engine()

        # Check store access
        self._check_access_to_storage(engine)

        # Set destination if not provided
        if dst is None:
            raise StoreError("Destination table name not provided.")

        # Write dataframe to db
        df.to_sql(dst, engine, index=False, **kwargs)

        # Close connection
        engine.dispose()

        # Return uri where dataframe was saved
        return f"sql://{self._get_schema()}.{dst}"

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
        try:
            return create_engine(connection_string, future=True)
        except Exception as ex:
            raise StoreError(
                f"Something wrong with connection string. Arguments: {str(ex.args)}"
            )

    def _get_scheme(self) -> str:
        """
        Get the URI scheme.

        Returns
        -------
        str
            The URI scheme.
        """
        return get_uri_scheme(self.uri)

    def _get_schema(self) -> str:
        """
        Get the name of the SQL schema from the URI.

        Returns
        -------
        str
            The name of the SQL schema.
        """
        return get_uri_netloc(self.uri)

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
        if self._get_scheme() != "sql":
            raise StoreError("Invalid URI scheme for sql store!")
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

    def get_root_uri(self) -> str:
        """
        Get the root URI of the store.

        Returns
        -------
        str
            The root URI of the store.
        """
        return f"sql://{self._get_schema()}"
