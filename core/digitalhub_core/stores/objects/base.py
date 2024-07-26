from __future__ import annotations

from abc import ABCMeta, abstractmethod
from pathlib import Path
from tempfile import mkdtemp
from typing import Literal

from digitalhub_core.utils.exceptions import StoreError
from digitalhub_core.utils.uri_utils import map_uri_scheme
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
    def download(self, src: str, dst: str | None = None, force: bool = False, overwrite: bool = False) -> str:
        """
        Method to download artifact from storage.
        """

    @abstractmethod
    def fetch_artifact(self, src: str, dst: str) -> str:
        """
        Method to fetch artifact from storage.
        """

    @abstractmethod
    def upload(self, src: str, dst: str | None = None) -> str:
        """
        Method to upload artifact to storage.
        """

    @abstractmethod
    def persist_artifact(self, src: str, dst: str) -> str:
        """
        Method to persist artifact in storage.
        """

    @abstractmethod
    def get_file_info(self, path: str, src_path: str | None = None) -> list:
        """
        Method to get file metadata.
        """

    ############################
    # Helpers methods
    ############################

    def _check_local_src(self, src: str) -> None:
        """
        Check if the source path is local.

        Parameters
        ----------
        src : str
            The source path.

        Returns
        -------
        None

        Raises
        ------
        StoreError
            If the source is not a local path.
        """
        if map_uri_scheme(src) != "local":
            raise StoreError(f"Source '{src}' is not a local path.")

    def _check_local_dst(self, dst: str) -> None:
        """
        Check if the local destination directory exists.

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
        if Path(dst).suffix != "":
            raise StoreError(f"Destination '{dst}' is not a directory.")

    def _check_overwrite(self, dst: str, overwrite: bool) -> None:
        """
        Check if destination path exists for overwrite.

        Parameters
        ----------
        dst : str
            Destination path as filename.
        overwrite : bool
            Specify if overwrite an existing file.

        Returns
        -------
        None

        Raises
        ------
        StoreError
            If destination path exists and overwrite is False.
        """
        if Path(dst).exists() and not overwrite:
            raise StoreError(f"Destination {dst} already exists.")

    @staticmethod
    def _build_path(path: str) -> None:
        """
        Get path from store path and path.

        Parameters
        ----------
        path : str
            The path to build.

        Returns
        -------
        None
        """
        pth = Path(path)
        if pth.suffix != "":
            pth = pth.parent
        pth.mkdir(parents=True, exist_ok=True)

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
        return str(Path(tmpdir) / Path(src).name)

    def _set_path_registry(self, src: str, path: str) -> None:
        """
        Set path in registry.

        Parameters
        ----------
        src : str
            Source to reference.
        path : str
            Path to set in registry.

        Returns
        -------
        None
        """
        self._registry[src] = path

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
