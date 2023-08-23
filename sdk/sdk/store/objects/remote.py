"""
Remote store module.
"""
from __future__ import annotations

import typing

import requests

from sdk.store.objects.base import Store
from sdk.utils.file_utils import build_path

if typing.TYPE_CHECKING:
    import pandas as pd


class RemoteStore(Store):
    """
    HTTP store class. It implements the Store interface and provides methods to fetch
    artifacts from remote HTTP based storage.
    """

    ############################
    # IO methods
    ############################

    def download(self, src: str, dst: str | None = None) -> str:
        """
        Method to download an artifact from the backend.

        Parameters
        ----------
        src : str
            The source location of the artifact.
        dst : str
            The destination of the artifact.

        Returns
        -------
        str
            The path of the downloaded artifact.
        """
        return self._registry.get(src, self.fetch_artifact(src, dst))

    def fetch_artifact(self, src: str, dst: str | None = None) -> str:
        """
        Method to fetch an artifact from the remote storage and to register
        it on the paths registry.
        If the destination is not provided, a temporary folder will be created.

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

        self._check_head(src)
        if dst is None:
            dst = self._build_temp(src)
        self._check_local_dst(dst)
        self._download_file(src, dst)
        return dst

    def upload(self, src: str, dst: str | None = None) -> str:
        """
        Method to upload an artifact to the backend. Please note that this method is not implemented
        since the remote store is not meant to upload artifacts.

        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError("Remote store does not support upload.")

    def persist_artifact(self, src: str, dst: str | None = None) -> str:
        """
        Method to persist an artifact. Note that this method is not implemented
        since the remote store is not meant to write artifacts.

        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError("Remote store does not support persist_artifact.")

    def write_df(self, df: pd.DataFrame, dst: str | None = None, **kwargs) -> str:
        """
        Method to write a dataframe to a file. Note that this method is not implemented
        since the remote store is not meant to write dataframes.

        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError("Remote store does not support write_df.")

    ############################
    # Private helper methods
    ############################

    @staticmethod
    def _check_head(src) -> None:
        """
        Check if the source exists.

        Parameters
        ----------
        src : str
            The source location.

        Returns
        -------
        None

        Raises
        ------
        HTTPError
            If an error occurs while checking the source.
        """
        r = requests.head(src, timeout=60)
        r.raise_for_status()

    @staticmethod
    def _download_file(url: str, dst: str) -> None:
        """
        Method to download a file from a given url.

        Parameters
        ----------
        url : str
            The url of the file to download.
        dst : str
            The destination of the file.

        Returns
        -------
        None
        """
        if not dst.endswith(".csv") or not dst.endswith(".parquet"):
            dst = build_path(dst, "temp.file")
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(dst, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

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
            False
        """
        return False
