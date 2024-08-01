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
        self.files = files
        if self.files is None:
            self.files = []

    def add_file(self, files: list) -> None:
        """
        Add a file to the status.

        Parameters
        ----------
        files : list
            Files to add.

        Returns
        -------
        None
        """
        for file in files:
            # Remove the file info if it already exists
            self.files = [f for f in self.files if (f["path"] != file["path"] or f["hash"] != file["hash"])]

            # Add the new file
            self.files.append(file)

    def get_file_paths(self) -> list[tuple[str, str]]:
        """
        Get the paths of the files in the status.

        Returns
        -------
        list[tuple[str, str]]
            Paths of the files in the status.
        """
        return [(f["path"], f["src_path"]) for f in self.files]
