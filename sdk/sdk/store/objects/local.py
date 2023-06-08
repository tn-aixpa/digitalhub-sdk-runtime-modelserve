from pathlib import Path
from typing import Optional

from sdk.store.objects.store import Store
from sdk.utils.file_utils import check_dir, check_path, copy_file, get_path, make_dir


class LocalStore(Store):
    def __init__(
        self,
        name: str,
        type: str,
        uri: str,
        tmp: str,
        config: Optional[dict] = None,
    ) -> None:
        super().__init__(name, type, uri, tmp, config)

    def fetch_artifact(self, src: str, dst: str) -> None:
        self._register_resource(f"{src}", src)
        return src

    def persist_artifact(self, src: str, dst: str, src_name: str) -> None:
        """
        Method to persist artifact in storage.
        """
        self._check_access_to_storage(dst, write=True)

        if src_name is not None:
            dst = get_path(dst, src_name)

        # Local file or dump string
        if isinstance(src, (str, Path)) and check_path(src):
            copy_file(src, dst)

        else:
            raise NotImplementedError

    def _check_access_to_storage(self, dst: str, write: bool = False) -> None:
        """
        Check if there is access to the path.

        Parameters
        ----------
        dst : str
            The path being checked.
        write : bool, optional
            Whether we want to check for writing permission. Default is False.

        Returns
        -------
        None
        """
        if write and not check_dir(dst):
            make_dir(dst)

    def _get_data(self, *args) -> None:
        """
        Placeholder method.

        Returns:
        --------
        None
        """
        ...

    def _store_data(self, *args) -> None:
        """
        Placeholder method.

        Returns:
        --------
        None
        """
        ...
