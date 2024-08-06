from __future__ import annotations

import typing
from pathlib import Path

from digitalhub_core.client.builder import get_client
from digitalhub_core.context.builder import set_context
from digitalhub_core.entities._base.crud import (
    create_entity_api_base,
    read_entity_api_base,
    read_entity_api_ctx,
    update_entity_api_base,
)
from digitalhub_core.entities._base.entity.base import Entity
from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.name import build_name
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.utils.exceptions import BackendError
from digitalhub_core.utils.generic_utils import get_timestamp
from digitalhub_core.utils.io_utils import write_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities.project.spec import ProjectSpec
    from digitalhub_core.entities.project.status import ProjectStatus

CTX_ENTITIES = []
FUNC_MAP = {}


class Project(Entity):
    """
    A class representing a project.
    """

    ENTITY_TYPE = EntityTypes.PROJECT.value

    def __init__(
        self,
        name: str,
        kind: str,
        metadata: Metadata,
        spec: ProjectSpec,
        status: ProjectStatus,
        user: str | None = None,
        local: bool = False,
    ) -> None:
        super().__init__(kind, metadata, spec, status, user)
        self.id = name
        self.name = name
        self.key = f"store://{name}"
        self.spec: ProjectSpec
        self.status: ProjectStatus

        # Add attributes to be used in the to_dict method
        self._obj_attr.extend(["id", "name"])

        # Set client
        self._client = get_client(local)

        # Set context
        set_context(self)

    ##############################
    #  Save / Refresh / Export
    ##############################

    def save(self, update: bool = False) -> Project:
        """
        Save entity into backend.

        Parameters
        ----------
        update : bool
            If True, the object will be updated.

        Returns
        -------
        Project
            Entity saved.
        """
        obj = self._refresh_to_dict()

        if not update:
            new_obj = create_entity_api_base(self._client, self.ENTITY_TYPE, obj)
            new_obj["local"] = self._client.is_local()
            self._update_attributes(new_obj)
            return self

        self.metadata.updated = obj["metadata"]["updated"] = get_timestamp()
        new_obj = update_entity_api_base(self._client, self.ENTITY_TYPE, obj)
        new_obj["local"] = self._client.is_local()
        self._update_attributes(new_obj)
        return self

    def refresh(self) -> Project:
        """
        Refresh object from backend.

        Returns
        -------
        Project
            Project object.
        """
        new_obj = read_entity_api_base(self._client, self.ENTITY_TYPE, self.name)
        new_obj["local"] = self._client.is_local()
        self._update_attributes(new_obj)
        return self

    def export(self, filename: str | None = None) -> None:
        """
        Export object as a YAML file. If the objects are not embedded, the objects are
        exported as a YAML file.

        Parameters
        ----------
        filename : str
            Name of the export YAML file. If not specified, the default value is used.

        Returns
        -------
        None
        """
        obj = self._refresh_to_dict()

        if filename is None:
            filename = f"{self.kind}_{self.name}.yml"
        pth = Path(self.spec.context) / filename
        pth.parent.mkdir(parents=True, exist_ok=True)
        write_yaml(pth, obj)

        for entity_type in CTX_ENTITIES:
            entity_list = obj.get("spec", {}).get(entity_type, [])
            if not entity_list:
                continue
            self._export_not_embedded(entity_list, entity_type)

    def _refresh_to_dict(self) -> dict:
        """
        Try to refresh object to collect entities related to project.

        Returns
        -------
        dict
            Entity object in dictionary format.
        """
        try:
            return self.refresh().to_dict()
        except BackendError:
            return self.to_dict()

    def _export_not_embedded(self, entity_list: list, entity_type: str) -> None:
        """
        Export project objects if not embedded.

        Parameters
        ----------
        entity_list : list
            Entity list.

        Returns
        -------
        None
        """
        for entity in entity_list:
            if not entity["metadata"]["embedded"]:
                obj: dict = read_entity_api_ctx(entity["key"])
                ent = FUNC_MAP[entity_type](obj)
                ent.export()

    ##############################
    #  Static interface methods
    ##############################

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
        name = build_name(obj.get("name"))
        kind = obj.get("kind")
        metadata = build_metadata(kind, **obj.get("metadata", {}))
        spec = build_spec(kind, validate=validate, **obj.get("spec", {}))
        status = build_status(kind, **obj.get("status", {}))
        user = obj.get("user")
        local = obj.get("local", False)
        return {
            "name": name,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
            "user": user,
            "local": local,
        }
