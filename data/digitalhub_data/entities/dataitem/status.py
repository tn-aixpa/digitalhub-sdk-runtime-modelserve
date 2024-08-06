from __future__ import annotations

from digitalhub_core.entities._base.status.material import MaterialStatus


class DataitemStatus(MaterialStatus):
    """
    Status class for dataitem entities.
    """

    def __init__(
        self,
        state: str,
        message: str | None = None,
        files: list[dict] | None = None,
        preview: dict | None = None,
        **kwargs,
    ) -> None:
        super().__init__(state, message, files)
        self.preview = preview


class DataitemStatusDataitem(DataitemStatus):
    """
    Status class for dataitem dataitem entities.
    """


class DataitemStatusTable(DataitemStatus):
    """
    Status class for dataitem table entities.
    """


class DataitemStatusIceberg(DataitemStatus):
    """
    Status class for dataitem iceberg entities.
    """
