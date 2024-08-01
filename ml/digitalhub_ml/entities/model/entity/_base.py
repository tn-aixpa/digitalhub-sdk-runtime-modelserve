from __future__ import annotations

import typing

from digitalhub_core.entities._base.entity.material import MaterialEntity
from digitalhub_ml.entities.entity_types import EntityTypes

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_ml.entities.model.spec import ModelSpec
    from digitalhub_ml.entities.model.status import ModelStatus


class Model(MaterialEntity):
    """
    A class representing a model.
    """

    ENTITY_TYPE = EntityTypes.MODEL.value

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: ModelSpec,
        status: ModelStatus,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)
        self.spec: ModelSpec
        self.status: ModelStatus
