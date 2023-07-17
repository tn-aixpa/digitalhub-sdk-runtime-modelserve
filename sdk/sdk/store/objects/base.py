"""
Store module.
"""
from abc import ABCMeta, abstractmethod
from typing import Optional

import pandas as pd


class ResourceRegistry(dict):
    """
    Registry object to keep track of resources fetched from a backend
    and their temporary local paths.
    """

    def set_resource(self, res_name: str, path: str) -> None:
        """
        Register resource.

        Parameters
        ----------
        res_name : str
            Resource name.
        path : str
            Resource path.

        Returns
        -------
        None
        """
        if res_name not in self:
            self[res_name] = path

    def get_resource(self, res_name: str) -> str | None:
        """
        Get resource path.

        Parameters
        ----------
        res_name : str
            Resource name.

        Returns
        -------
        str
            Resource path.
        """
        return self.get(res_name)

    def clean_all(self) -> None:
        """
        Clean all resources.

        Returns
        -------
        None
        """
        self.clear()


class Store(metaclass=ABCMeta):
    """
    Store abstract class.
    """

    def __init__(
        self,
        name: str,
        store_type: str,
        uri: str,
        config: Optional[dict] = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        name : str
            Store name.
        store_type : str
            Store type.
        uri : str
            Store URI.
        config : Optional[dict]
            Store configuration, by default None

        Returns
        -------
        None
        """
        self.name = name
        self.type = store_type
        self.uri = uri
        self.config = config
        self.registry = ResourceRegistry()

        self._validate_uri()

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
    def write_df(self, df: pd.DataFrame, dst: str, **kwargs) -> str:
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
    # Interface helpers methods
    ############################

    @abstractmethod
    def _validate_uri(self) -> None:
        """
        Method to validate URI.
        """

    @staticmethod
    @abstractmethod
    def is_local() -> bool:
        """
        Method to check if store is local.
        """

    @abstractmethod
    def get_root_uri(self) -> str:
        """
        Method to get root URI.
        """

    ############################
    # Resource registry methods
    ############################

    def _register_resource(self, key: str, path: str) -> None:
        """
        Register a resource in the registry.
        """
        self.registry.set_resource(key, path)

    def get_resource(self, key: str) -> str | None:
        """
        Get a resource from the registry.
        """
        return self.registry.get_resource(key)
