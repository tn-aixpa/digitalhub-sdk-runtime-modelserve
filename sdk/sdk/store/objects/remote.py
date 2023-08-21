"""
Remote store module.
"""
from __future__ import annotations

import typing
from tempfile import mkdtemp

import requests

from sdk.store.objects.base import Store
from sdk.utils.file_utils import get_dir, check_make_dir
from sdk.utils.exceptions import StoreError
from sdk.utils.uri_utils import (
    get_name_from_uri,
    get_uri_netloc,
    get_uri_scheme,
)

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
        return self.fetch_artifact(src, dst)

    def fetch_artifact(self, src: str, dst: str | None = None) -> str:
        """
        Method to fetch an artifact from the remote storage and to register
        it on the paths registry.

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

        # Check if source exists
        self._check_head(src)

        # Rebuild destination if not provided
        if dst is None:
            tmpdir = mkdtemp()
            dst = f"{tmpdir}/{get_name_from_uri(src)}"
            self._register_resource(f"{src}", dst)

        # Check if local destination exists and make folders.
        self._check_local_dst(dst)

        # If file is not csv or parquet, append temp as file name
        if not dst.endswith(".csv") or not dst.endswith(".parquet"):
            dst = f"{dst}/temp.file"

        # Fetch artifact
        self._download_file(src, dst)

        return dst

    def upload(self, src: str, dst: str | None = None) -> str:
        """
        Method to upload an artifact to the backend. Please note that this method is not implemented
        since the local store is not meant to upload artifacts.

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
        StoreError
            If the source does not exist.
        """
        r = requests.head(src, timeout=60)
        if r.status_code != 200:
            raise StoreError(f"Source {src} does not exist.")

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
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(dst, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

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
            If the URI scheme is not 'http' or 'https'.

        """
        scheme = get_uri_scheme(self.uri)
        if scheme not in ["http", "https"]:
            raise StoreError(
                f"Invalid URI scheme for remote store: {scheme}. Should be 'http' or 'https'."
            )

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
        Return base url from the store URI.

        Returns
        -------
        str
            The base url.
        """
        return f"{get_uri_scheme(self.uri)}://{get_uri_netloc(self.uri)}"
