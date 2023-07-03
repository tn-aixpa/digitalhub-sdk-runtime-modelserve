"""
Local store module.
"""
from __future__ import annotations

import typing

from sdk.store.objects.store import Store
from sdk.utils.file_utils import check_dir, copy_file, get_dir, make_dir
from sdk.utils.uri_utils import get_name_from_uri

if typing.TYPE_CHECKING:
    import pandas as pd


class LocalStore(Store):
    """
    S3 store class. It implements the Store interface and provides methods to fetch and persist
    artifacts on local filesystem based storage.
    """

    ############################
    # IO methods
    ############################

    def upload(self, *args, **kwargs) -> None:
        """
        Method to upload an artifact to the backend. Please note that this method is not implemented
        since the local store is not meant to upload artifacts.

        Parameters
        ----------
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError("Local store does not support upload.")

    def download(self, *args, **kwargs) -> None:
        """
        Method to download an artifact from the backend. Please note that this method is not
        implemented since the local store is not meant to download artifacts.

        Parameters
        ----------
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError(
            "Local store does not support download. Use as_file() instead."
        )

    def fetch_artifact(self, src: str, dst: str = None) -> str:
        """
        Method to fetch an artifact from the backend and to register it on the paths registry.

        Parameters
        ----------
        src : str
            The source location of the artifact.
        dst : str, optional
            The destination of the artifact.

        Returns
        -------
        str
            Returns the path of the artifact.
        """
        if dst is not None:
            # Check access to destination
            self._check_dir(get_dir(dst))

            # Copy file and register resource
            copy_file(src, dst)
            self._register_resource(f"{src}", dst)

            # In case of a directory, return the filename
            # from source path, because we simply copied
            # the file into the destination directory
            if get_name_from_uri(dst) == "":
                dst = f"{dst}/{get_name_from_uri(src)}"
            return dst

        # If destination is not provided, return the source path
        # we don't copy the file anywhere
        return src

    def persist_artifact(self, src: str, dst: str = None) -> None:
        """
        Method to persist (copy) an artifact on local filesystem.

        Parameters
        ----------
        src : str
            The source location of the artifact.
        dst : str
            The destination of the artifact.
        src_name : str
            The name of the artifact.

        Returns
        -------
        None
        """
        # Set destination if not provided
        if dst is None:
            file = get_name_from_uri(src)
            base_path = get_dir(self.uri)
            dst = f"{base_path}/{file}"

        # Check access to destination
        self._check_dir(get_dir(dst))

        # Local file or dump string
        copy_file(src, dst)
        return dst

    def write_df(self, df: pd.DataFrame, dst: str, **kwargs) -> None:
        """
        Method to write a dataframe to a file.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to write.
        dst : str
            The destination of the dataframe.
        **kwargs
            Keyword arguments to pass to to_parquet() method.

        Returns
        -------
        None
        """
        # Check access to destination
        self._check_dir(get_dir(dst))

        # Write dataframe to file
        df.to_parquet(dst, index=False, **kwargs)

    ############################
    # Private helper methods
    ############################

    @staticmethod
    def _check_dir(dst: str) -> None:
        """
        Check if there is access to the path.

        Parameters
        ----------
        dst : str
            The path to check.

        Returns
        -------
        None
        """
        if not check_dir(dst):
            make_dir(dst)

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

    def get_root_uri(self) -> str:
        """
        Get the root URI of the store.

        Returns
        -------
        str
            The root URI of the store.
        """
        return get_dir(self.uri)
