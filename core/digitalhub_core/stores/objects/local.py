from __future__ import annotations

import shutil
from pathlib import Path

from digitalhub_core.stores.objects.base import Store, StoreConfig
from digitalhub_core.utils.exceptions import StoreError
from digitalhub_core.utils.file_utils import get_file_info_from_local
from digitalhub_core.utils.uri_utils import check_local_path


class LocalStoreConfig(StoreConfig):
    """
    Local store configuration class.
    """

    path: str
    """Local path."""


class LocalStore(Store):
    """
    Local store class. It implements the Store interface and provides methods to fetch and persist
    artifacts on local filesystem based storage.
    """

    def __init__(self, name: str, store_type: str, config: LocalStoreConfig) -> None:
        super().__init__(name, store_type)
        self.config = config

    ############################
    # IO methods
    ############################

    def download(self, src: str, dst: str | None = None, force: bool = False, overwrite: bool = False) -> str:
        """
        Download an artifact from local storage.

        See Also
        --------
        fetch_artifact
        """
        if dst is None:
            return src

        self._check_local_dst(dst)
        self._check_overwrite(dst, overwrite)

        if force:
            return self.fetch_artifact(src, dst)
        return self._registry.get(src, self.fetch_artifact(src, dst))

    def fetch_artifact(self, src: str, dst: str) -> str:
        """
        Method to fetch an artifact from backend and to register it on the paths registry.
        If destination is not provided, return the source path, otherwise the path of the copied
        file.

        Parameters
        ----------
        src : str
            The source location of the artifact.
        dst : str
            The destination of the artifact.

        Returns
        -------
        str
            Returns the path of the artifact.
        """
        if Path(src).suffix == "":
            path = shutil.copytree(src, dst)
        else:
            self._build_path(dst)
            path = shutil.copy(src, dst)
        self._set_path_registry(src, path)
        return path

    def upload(self, src: str, dst: str | None = None) -> str:
        """
        Upload an artifact to local storage.

        See Also
        --------
        persist_artifact
        """
        self._check_local_src(src)
        if dst is None:
            dst = str(Path(self.config.path) / Path(src).name)
        self._check_local_dst(dst)
        return self.persist_artifact(src, dst)

    def persist_artifact(self, src: str, dst: str) -> str:
        """
        Method to persist (copy) an artifact on local filesystem.
        If destination is not provided, the artifact is written to the default
        store path with source name.

        Parameters
        ----------
        src : str
            The source location of the artifact.
        dst : str
            The destination of the artifact.

        Returns
        -------
        dst
            Returns the URI of the artifact.
        """
        return shutil.copy(src, dst)

    def get_file_info(self, path: str, src_path: str | None = None) -> dict | None:
        """
        Method to get file metadata.

        Parameters
        ----------
        path : str
            The path of the file.
        src_path : str
            The source path of the file.

        Returns
        -------
        dict
            Returns the metadata of the file.
        """
        return get_file_info_from_local(path, src_path)

    ############################
    # Private helper methods
    ############################

    def _check_local(self, path: str) -> None:
        """
        Check through URI scheme if given path is local or not.

        Parameters
        ----------
        path : str
            Path of some source.

        Returns
        -------
        None

        Raises
        ------
        StoreError
            If source path is not local.
        """
        if not check_local_path(path):
            raise StoreError("Only local paths are supported for source paths.")

    ############################
    # Store interface methods
    ############################

    @staticmethod
    def is_local() -> bool:
        """
        Check if the store is local.

        Returns
        -------
        bool
            True
        """
        return True
