from __future__ import annotations

from pathlib import Path

import requests
from digitalhub_core.stores.objects.base import Store, StoreConfig


class RemoteStoreConfig(StoreConfig):
    """
    Remote store configuration class.
    """


class RemoteStore(Store):
    """
    HTTP store class. It implements the Store interface and provides methods to fetch
    artifacts from remote HTTP based storage.
    """

    def __init__(self, name: str, store_type: str, config: RemoteStoreConfig) -> None:
        super().__init__(name, store_type)
        self.config = config

    ############################
    # IO methods
    ############################

    def download(self, src: str, dst: str | None = None, force: bool = False, overwrite: bool = False) -> str:
        """
        Download an artifact from HTTP(s) storage.

        See Also
        --------
        fetch_artifact
        """
        if dst is None:
            dst = self._build_temp("remote")
        else:
            self._check_local_dst(dst)
            self._check_overwrite(dst, overwrite)
            self._build_path(dst)

        if Path(dst).suffix == "":
            dst = str(Path(dst) / "temp.file")

        if force:
            return self.fetch_artifact(src, dst)
        return self._registry.get(src, self.fetch_artifact(src, dst))

    def fetch_artifact(self, src: str, dst: str) -> str:
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
        path = self._download_file(src, dst)
        self._set_path_registry(src, path)
        return path

    def upload(self, src: str, dst: str | None = None) -> list[tuple[str, str]]:
        """
        Upload an artifact to HTTP(s) storage.

        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError("Remote store does not support upload.")

    def get_file_info(self, paths: list[tuple[str, str]]) -> list[dict]:
        """
        Get file information from HTTP(s) storage.

        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError("Remote store does not support get_file_info.")

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

    def _download_file(self, url: str, dst: str) -> str:
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
        str
            The path of the downloaded file.
        """
        self._check_head(url)
        self._check_local_dst(dst)
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(dst, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return dst
