from __future__ import annotations

import typing
from typing import Any

from digitalhub_core.entities.project.entity.core import CTX_ENTITIES, FUNC_MAP, ProjectCore
from digitalhub_data.entities.dataitem.crud import (
    dataitem_from_dict,
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
FUNC_MAP[DATAITEMS] = dataitem_from_dict


class ProjectData(ProjectCore):

    """
    ProjectData class.
    """

    ##############################
    #  Dataitems
    ##############################

    def new_dataitem(
        self,
        name: str,
        kind: str,
        uuid: str | None = None,
        description: str | None = None,
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
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object must be embedded in project.
        path : str
            Object path on local file system or remote storage.
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
            uuid=uuid,
            description=description,
            labels=labels,
            embedded=embedded,
            path=path,
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
            Destination path of the dataitem. If not provided, it's generated.
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
