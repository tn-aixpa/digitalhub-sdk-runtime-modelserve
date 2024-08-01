from __future__ import annotations

import typing
from typing import Any

from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.name import build_name
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities.project.entity import CTX_ENTITIES, FUNC_MAP, ProjectCore
from digitalhub_data.entities.dataitem.crud import (
    create_dataitem_from_dict,
    delete_dataitem,
    get_dataitem,
    list_dataitems,
    log_dataitem,
    new_dataitem,
)
from digitalhub_data.entities.entity_types import EntityTypes

if typing.TYPE_CHECKING:
    from digitalhub_data.entities.dataitem.entity._base import Dataitem


DATAITEMS = EntityTypes.DATAITEM.value

CTX_ENTITIES.append(DATAITEMS)
FUNC_MAP[DATAITEMS] = create_dataitem_from_dict


class ProjectData(ProjectCore):

    """
    ProjectData class.
    """

    #############################
    #  Dataitems
    #############################

    def new_dataitem(
        self,
        name: str,
        kind: str,
        uuid: str | None = None,
        description: str | None = None,
        git_source: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = True,
        path: str | None = None,
        **kwargs,
    ) -> Dataitem:
        """
        Create a new object instance.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        uuid : str
            ID of the object (UUID4).
        description : str
            Description of the object (human readable).
        git_source : str
            Remote git source for object.
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object must be embedded in project.
        path : str
            Object path on local file system or remote storage.
            If not provided, it's generated.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Dataitem
            Object instance.
        """
        obj = new_dataitem(
            project=self.name,
            name=name,
            kind=kind,
            path=path,
            uuid=uuid,
            description=description,
            git_source=git_source,
            labels=labels,
            embedded=embedded,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_dataitem(
        self,
        identifier: str,
        entity_id: str | None = None,
        **kwargs,
    ) -> Dataitem:
        """
        Get object from backend.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Dataitem
            Instance of Dataitem class.
        """
        obj = get_dataitem(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def delete_dataitem(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        **kwargs,
    ) -> None:
        """
        Delete a Dataitem from project.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity.
            Use entity name instead of entity key as identifier.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        delete_dataitem(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            delete_all_versions=delete_all_versions,
            **kwargs,
        )
        self.refresh()

    def list_dataitems(self, **kwargs) -> list[dict]:
        """
        List dataitems associated with the project.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            List of objects related to project.
        """
        return list_dataitems(self.name, **kwargs)

    def log_dataitem(
        self,
        name: str,
        kind: str,
        path: str | None = None,
        data: Any | None = None,
        extension: str | None = None,
        **kwargs,
    ) -> Dataitem:
        """
        Log a dataitem to the project.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        path : str
            Destination path of the dataitem.
        data : Any
            Dataframe to log.
        extension : str
            Extension of the dataitem.
        **kwargs : dict
            New dataitem parameters.

        Returns
        -------
        Dataitem
            Object instance.
        """
        obj = log_dataitem(
            project=self.name,
            name=name,
            kind=kind,
            path=path,
            data=data,
            extension=extension,
            **kwargs,
        )
        self.refresh()
        return obj

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
        # Override methods to search in digitalhub_data
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
