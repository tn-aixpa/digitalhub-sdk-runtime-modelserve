"""
Store module.
"""
from abc import ABCMeta, abstractmethod

import pandas as pd

from sdk.utils.exceptions import StoreError
from sdk.utils.file_utils import check_make_dir, get_dir
from sdk.utils.uri_utils import get_uri_scheme


class _ResourceRegistry(dict):
    """
    Registry object to keep track of resources fetched from a backend
    and their temporary local paths.
    It is used to avoid fetching the same resource multiple times.
    This class is private and should not be used directly.
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
        config: dict | None = None,
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
        config : dict | None
            Store configuration, by default None

        Returns
        -------
        None
        """
        self.name = name
        self.type = store_type
        self.uri = uri
        self.config = config if config is not None else {}

        # Private attributes
        self._registry = _ResourceRegistry()

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
    # Interface helpers methods
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
        if get_uri_scheme(dst) in ["", "file"]:
            dst_dir = get_dir(dst)
            check_make_dir(dst_dir)
            return
        raise StoreError(f"Destination {dst} is not a local path.")

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
        self._registry.set_resource(key, path)

    def get_resource(self, key: str) -> str | None:
        """
        Get a resource from the registry.
        """
        return self._registry.get_resource(key)
