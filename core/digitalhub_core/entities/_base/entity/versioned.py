from __future__ import annotations

import typing

from digitalhub_core.entities._base.entity.context import ContextEntity
from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.name import build_name
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities._builders.uuid import build_uuid
from digitalhub_core.utils.io_utils import write_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities._base.spec.base import Spec
    from digitalhub_core.entities._base.status.base import Status


class VersionedEntity(ContextEntity):
    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: Spec,
        status: Status,
        user: str | None = None,
    ) -> None:
        super().__init__(project, kind, metadata, spec, status, user)
        self.name = name
        self.id = uuid
        self.key = f"store://{project}/{self.ENTITY_TYPE}/{kind}/{name}:{uuid}"

        # Add attributes to be used in the to_dict method
        self._obj_attr.extend(["name", "id"])

    def export(self, filename: str | None = None) -> None:
        """
        Export object as a YAML file.

        Parameters
        ----------
        filename : str
            Name of the export YAML file. If not specified, the default value is used.

        Returns
        -------
        None
        """
        obj = self.to_dict()
        if filename is None:
            filename = f"{self.ENTITY_TYPE}-{self.name}-{self.id}.yml"
        pth = self._context().root / filename
        write_yaml(pth, obj)

    @staticmethod
    def _parse_dict(obj: dict, validate: bool = True) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        entity : str
            Entity type.
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        project = obj.get("project")
        kind = obj.get("kind")
        name = build_name(obj.get("name"))
        uuid = build_uuid(obj.get("id"))
        metadata = build_metadata(kind, **obj.get("metadata", {}))
        spec = build_spec(kind, validate=validate, **obj.get("spec", {}))
        status = build_status(kind, **obj.get("status", {}))
        user = obj.get("user")
        return {
            "project": project,
            "name": name,
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
            "user": user,
        }
