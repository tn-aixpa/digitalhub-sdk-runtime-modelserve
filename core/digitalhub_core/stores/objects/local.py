from __future__ import annotations

import shutil
from pathlib import Path

from digitalhub_core.stores.objects.base import Store, StoreConfig
from digitalhub_core.utils.exceptions import StoreError
from digitalhub_core.utils.file_utils import get_file_info_from_local


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

    def download(
        self,
        src: str,
        dst: str | None = None,
        force: bool = False,
        overwrite: bool = False,
    ) -> str:
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

    def upload(self, src: str, dst: str | None = None) -> list[tuple[str, str]]:
        """
        Upload an artifact to storage.

        Parameters
        ----------
        src : str
            The source location of the artifact on local filesystem.
        dst : str
            The destination of the artifact on storage.

        Returns
        -------
        list[tuple[str, str]]
            Returns the list of source and destination paths of the
            uploaded artifacts.
        """
        # Destination handling

        # If no destination is provided use store path,
        # otherwise check if destination is local or not
        if dst is None:
            dst = self.config.path
            Path(dst).mkdir(parents=True, exist_ok=True)
        else:
            self._check_local_dst(dst)

        # Create destination directory if it doesn't exist
        dst_pth = Path(dst)
        if dst_pth.suffix == "":
            dst_pth.mkdir(parents=True, exist_ok=True)
        else:
            dst_pth.parent.mkdir(parents=True, exist_ok=True)

        # Source handling
        self._check_local_src(src)
        src_pth = Path(src)

        if src_pth.is_dir():
            if not dst_pth.is_dir():
                raise StoreError("Destination must be a directory if the source is a directory.")
            return self._copy_files(src_pth, dst_pth)
        return self._copy_file(src_pth, dst_pth)

    def get_file_info(self, paths: list[tuple[str, str]]) -> list[dict]:
        """
        Method to get file metadata.

        Parameters
        ----------
        paths : list
            The list of destination and source paths.

        Returns
        -------
        list[dict]
            Returns files metadata.
        """
        return [get_file_info_from_local(*p) for p in paths]

    ############################
    # Private I/O methods
    ############################

    def _copy_files(self, src: Path, dst: Path) -> list[tuple[str, str]]:
        """
        Copy files from source to destination.

        Parameters
        ----------
        src : Path
            The source path.
        dst : Path
            The destination path.

        Returns
        -------
        list[tuple[str, str]]
            Returns the list of destination and source paths of the
            copied files.
        """
        paths = []
        files = [i for i in src.rglob("*") if i.is_file()]
        for f in files:
            if f.is_absolute():
                f = Path(*f.parts[1:])
            dst = dst / f
            paths.append(self._copy_file(f, dst))
        return paths

    def _copy_file(self, src: Path, dst: Path) -> tuple[str, str]:
        """
        Copy file from source to destination.

        Parameters
        ----------
        src : Path
            The source path.
        dst : Path
            The destination path.

        Returns
        -------
        tuple[str, str]
            Returns the destination and source paths of the
            copied file.
        """
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dst)
        return str(dst), str(src)

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
