"""
Local store module.
"""
from typing import Optional

from sdk.store.objects.store import Store
from sdk.utils.file_utils import check_dir, copy_file, get_dir, make_dir
from sdk.utils.uri_utils import get_name_from_uri


class LocalStore(Store):
    """
    S3 store class. It implements the Store interface and provides methods to fetch and persist
    artifacts on local filesystem based storage.
    """

    def __init__(
        self,
        name: str,
        type: str,
        uri: str,
        config: Optional[dict] = None,
    ) -> None:
        """
        Constructor.

        See Also
        --------
        Store.__init__
        """
        super().__init__(name, type, uri, config)

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
            dst = f"{base_path}/artifacts/{file}"

        # Check access to destination
        self._check_dir(get_dir(dst))

        # Local file or dump string
        copy_file(src, dst)
        return dst

    def _check_dir(self, dst: str) -> None:
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
