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

    ##############################
    # IO methods
    ##############################

    def download(
        self,
        src: list[tuple[str, str | None]],
        dst: str | None = None,
        overwrite: bool = False,
    ) -> list[str]:
        """
        Download an artifact from local storage.

        Parameters
        ----------
        """
        paths = []

        # Handle destination

        # If destination is not specified, return the source path
        if dst is None:
            for i in src:
                self._check_local_src(i[0])
                p = Path(i[0])
                if p.is_file():
                    paths.append(str(p))
                elif p.is_dir():
                    files = [str(i) for i in p.rglob("*") if i.is_file()]
                    paths.extend(files)
            return paths

        # Otherwise, check if the destination is local,
        else:
            self._check_local_dst(dst)

        dst_pth = Path(dst)
        self._build_path(dst_pth)

        # Handle src
        for s in src:

            # Check if source is local
            self._check_local_src(s[0])
            src_pth = Path(s[0])

            # If an original source path is specified try to reconstruct
            # the path under the new destination
            if s[1] is not None:
                self._check_local_src(s[1])
                tree_path = Path(s[1])
                dst_pth = self._rebuild_path(dst_pth, tree_path)

            # If source is a directory, copy recursively
            if src_pth.is_dir():
                p = self._copy_dir(src_pth, dst_pth, overwrite)
            else:
                p = [self._copy_file(src_pth, dst_pth, overwrite)]

            paths.extend(p)

        return paths

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

        # If no destination is provided use store path
        if dst is None:
            dst = self.config.path

        self._check_local_dst(dst)
        dst_pth = Path(dst)
        self._build_path(dst_pth)

        # Source handling
        self._check_local_src(src)
        src_pth = Path(src)

        if src_pth.is_dir():
            if not dst_pth.is_dir():
                raise StoreError("Destination must be a directory if the source is a directory.")
            return self._get_src_dst_files(src_pth, dst_pth)
        return [self._get_src_dst_file(src_pth, dst_pth)]

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

    ##############################
    # Private I/O methods
    ##############################

    def _get_src_dst_files(self, src: Path, dst: Path) -> list[tuple[str, str]]:
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
        return [self._get_src_dst_file(i, dst) for i in src.rglob("*") if i.is_file()]

    def _get_src_dst_file(self, src: Path, dst: Path) -> str:
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
        str
        """
        dst_pth = self._copy_file(src, dst, True)
        return str(dst_pth), str(src)

    def _copy_dir(self, src: Path, dst: Path, overwrite: bool) -> list[str]:
        """
        Download file from source to destination.

        Parameters
        ----------
        src : Path
            The source path.
        dst : Path
            The destination path.

        Returns
        -------
        list[str]
        """
        dst = self._rebuild_path(dst, src)
        shutil.copytree(src, dst, dirs_exist_ok=overwrite)
        return [str(i) for i in dst.rglob("*") if i.is_file()]

    def _copy_file(self, src: Path, dst: Path, overwrite: bool) -> str:
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
        str
        """
        dst = self._rebuild_path(dst, src)
        self._check_overwrite(dst, overwrite)
        return str(shutil.copy2(src, dst))

    def _rebuild_path(self, dst: Path, src: Path) -> Path:
        """
        Rebuild path.

        Parameters
        ----------
        dst : Path
            The destination path.
        src : Path
            The source path.

        Returns
        -------
        Path
            The rebuilt path.
        """
        if dst.is_dir():
            if src.is_absolute():
                raise StoreError("Source must be a relative path if the destination is a directory.")
            dst = dst / src
        self._build_path(dst)
        return dst
