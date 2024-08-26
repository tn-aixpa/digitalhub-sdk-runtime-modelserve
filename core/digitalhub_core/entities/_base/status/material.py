from __future__ import annotations

from digitalhub_core.entities._base.status.base import Status


class MaterialStatus(Status):
    """
    Material Status class.
    """

    def __init__(
        self,
        state: str,
        message: str | None = None,
        files: list[dict] | None = None,
    ) -> None:
        super().__init__(state, message)
        self.files: list[dict] | None = files

    def add_files_info(self, files: list[dict] | None = None) -> None:
        """
        Add a file to the status.

        Parameters
        ----------
        files : list[dict]
            Files to add.

        Returns
        -------
        None
        """
        if isinstance(files, list):
            if files:
                self.files = files

    def get_file_paths(self) -> list[tuple[str, str]]:
        """
        Get the paths of the files in the status.

        Returns
        -------
        list[tuple[str, str]]
            Paths of the files in the status.
        """
        if self.files is None:
            return []
        return [(f.get("path"), f.get("src_path")) for f in self.files]
