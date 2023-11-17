"""
Store module.
"""
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from tempfile import mkdtemp
from typing import Literal

import pandas as pd
from digitalhub_core.utils.exceptions import StoreError
from digitalhub_core.utils.file_utils import build_path, make_dir
from digitalhub_core.utils.uri_utils import get_name_from_uri, map_uri_scheme
from pydantic import BaseModel


class Store(metaclass=ABCMeta):
    """
    Store abstract class.
    """

    def __init__(self, name: str, store_type: str) -> None:
        """
        Constructor.

        Parameters
        ----------
        name : str
            Store name.
        store_type : str
            Store type. Used to choose the right store implementation.
        uri : str
            Store URI.

        Returns
        -------
        None
        """
        self.name = name
        self.type = store_type

        # Private attributes
        self._registry: dict[str, str] = {}

    ############################
    # IO methods
    ############################

    @abstractmethod
    def download(self, src: str, dst: str | None = None) -> str:
        """
        Method to download artifact from storage.
        """

    @abstractmethod
    def fetch_artifact(self, src: str, dst: str | None = None) -> str:
        """
        Method to fetch artifact from storage.
        """

    @abstractmethod
    def upload(self, src: str, dst: str | None = None) -> str:
        """
        Method to upload artifact to storage.
        """

    @abstractmethod
    def persist_artifact(self, src: str, dst: str | None = None) -> str:
        """
        Method to persist artifact in storage.
        """

    @abstractmethod
    def write_df(self, df: pd.DataFrame, dst: str | None = None, **kwargs) -> str:
        """
        Write pandas DataFrame as parquet or csv.
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

        Raises
        ------
        ValueError
            If format is not supported.
        """
        if extension == "csv":
            return pd.read_csv(path, **kwargs)
        if extension == "parquet":
            return pd.read_parquet(path, **kwargs)
        raise ValueError(f"Format {extension} not supported.")

    ############################
    # Helpers methods
    ############################

    @staticmethod
    def _check_local_dst(dst: str) -> None:
        """
        Check if the local destination directory exists. Create in case it does not.

        Parameters
        ----------
        dst : str
            The destination directory.

        Returns
        -------
        None

        Raises
        ------
        StoreError
            If the destination is not a local path.
        """
        if map_uri_scheme(dst) != "local":
            raise StoreError(f"Destination '{dst}' is not a local path.")
        make_dir(dst)

    def _build_temp(self, src: str) -> str:
        """
        Build a temporary path.

        Parameters
        ----------
        src : str
            Source filename.

        Returns
        -------
        str
            Temporary path.
        """
        tmpdir = mkdtemp()
        dst = build_path(tmpdir, get_name_from_uri(src))
        self._registry[src] = dst
        return dst

    @staticmethod
    @abstractmethod
    def is_local() -> bool:
        """
        Method to check if store is local.
        """


class StoreConfig(BaseModel):
    """
    Store configuration base class.
    """


class StoreParameters(BaseModel):
    """
    Store configuration class.
    """

    name: str
    """Store id."""

    type: Literal["local", "s3", "remote", "sql"]
    """Store type to instantiate."""

    config: StoreConfig = None
    """Configuration for the store."""

    is_default: bool = False
    """Flag to determine if the store is the default one."""
