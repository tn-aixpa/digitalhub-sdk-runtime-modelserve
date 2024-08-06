from __future__ import annotations

import typing
from pathlib import Path

from digitalhub_core.entities._base.entity.material import MaterialEntity
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.uri_utils import map_uri_scheme
from digitalhub_data.entities.entity_types import EntityTypes

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_data.entities.dataitem.spec import DataitemSpec
    from digitalhub_data.entities.dataitem.status import DataitemStatus


class Dataitem(MaterialEntity):
    """
    A class representing a dataitem.
    """

    ENTITY_TYPE = EntityTypes.DATAITEM.value

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: DataitemSpec,
        status: DataitemStatus,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)
        self.spec: DataitemSpec
        self.status: DataitemStatus

    ##############################
    #  Private helper methods
    ##############################

    @staticmethod
    def _get_extension(path: str, file_format: str | None = None) -> str:
        """
        Get extension of path.

        Parameters
        ----------
        path : str
            Path to get extension from.
        file_format : str
            File format.

        Returns
        -------
        str
            File extension.

        Raises
        ------
        EntityError
            If file format is not supported.
        """
        if file_format is not None:
            return file_format

        scheme = map_uri_scheme(path)
        if scheme == "sql":
            return "parquet"

        ext = Path(path).suffix[1:]
        if ext is not None:
            return ext
        raise EntityError("Unknown file format. Only csv and parquet are supported.")
