from __future__ import annotations

import typing

from digitalhub_core.entities._base.entity.material import MaterialEntity
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities.artifact.spec import ArtifactSpec
    from digitalhub_core.entities.artifact.status import ArtifactStatus


class Artifact(MaterialEntity):
    """
    A class representing a artifact.

    Artifacts are (binary) objects stored in one of the artifact
    stores of the platform, and available to every process, module
    and component as files.
    """

    ENTITY_TYPE = EntityTypes.ARTIFACT.value

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: ArtifactSpec,
        status: ArtifactStatus,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: ArtifactSpec
        self.status: ArtifactStatus

    ##############################
    #  Artifacts Methods
    ##############################

    def upload(self, source: str | None = None) -> None:
        """
        Upload artifact from given local path to spec path destination.

        Parameters
        ----------
        source : str
            Source path is the local path of the artifact.

        Returns
        -------
        None
        """
        src = source if source is not None else self.spec.src_path
        if src is None:
            raise EntityError("Source path is not specified.")
        return super().upload(src)
