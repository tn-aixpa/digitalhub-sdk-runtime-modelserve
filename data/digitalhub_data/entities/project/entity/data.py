from __future__ import annotations

import typing
from typing import Any

from digitalhub_core.entities.project.entity.core import CTX_ENTITIES, FUNC_MAP, ProjectCore
from digitalhub_data.entities.dataitem.crud import (
    dataitem_from_dict,
    delete_dataitem,
    get_dataitem,
    get_dataitem_versions,
    import_dataitem,
    list_dataitems,
    log_dataitem,
    new_dataitem,
    update_dataitem,
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
        Create a new object.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        uuid : str
            ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object spec must be embedded in project spec.
        path : str
            Object path on local file system or remote storage. It is also the destination path of upload() method.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Dataitem
            Object instance.

        Examples
        --------
        >>> obj = project.new_dataitem(name="my-dataitem",
        >>>                            kind="dataitem",
        >>>                            path="s3://my-bucket/my-key")
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

    def log_dataitem(
        self,
        name: str,
        kind: str,
        source: str | None = None,
        data: Any | None = None,
        extension: str | None = None,
        path: str | None = None,
        **kwargs,
    ) -> Dataitem:
        """
        Create and upload an object.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        data : Any
            Dataframe to log.
        extension : str
            Extension of the dataitem.
        source : str
            Dataitem location on local path.
        data : Any
            Dataframe to log. Alternative to source.
        extension : str
            Extension of the output dataframe.
        path : str
            Destination path of the dataitem. If not provided, it's generated.
        **kwargs : dict
            New dataitem spec parameters.

        Returns
        -------
        Dataitem
            Object instance.

        Examples
        --------
        >>> obj = project.log_dataitem(name="my-dataitem",
        >>>                            kind="table",
        >>>                            data=df)
        """
        obj = log_dataitem(
            project=self.name,
            name=name,
            kind=kind,
            path=path,
            source=source,
            data=data,
            extension=extension,
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
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Dataitem
            Object instance.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_dataitem("store://my-dataitem-key")

        Using entity name:
        >>> obj = project.get_dataitem("my-dataitem-name"
        >>>                            entity_id="my-dataitem-id")
        """
        obj = get_dataitem(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_dataitem_versions(
        self,
        identifier: str,
        **kwargs,
    ) -> list[Dataitem]:
        """
        Get object versions from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Dataitem]
            List of object instances.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_dataitem_versions("store://my-dataitem-key")

        Using entity name:
        >>> obj = project.get_dataitem_versions("my-dataitem-name")
        """
        return get_dataitem_versions(identifier, project=self.name, **kwargs)

    def list_dataitems(self, **kwargs) -> list[Dataitem]:
        """
        List all latest version objects from backend.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Dataitem]
            List of object instances.

        Examples
        --------
        >>> objs = project.list_dataitems()
        """
        return list_dataitems(self.name, **kwargs)

    def import_dataitem(
        self,
        file: str,
        **kwargs,
    ) -> Dataitem:
        """
        Import object from a YAML file.

        Parameters
        ----------
        file : str
            Path to YAML file.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Dataitem
            Object instance.

        Examples
        --------
        >>> obj = project.import_dataitem("my-dataitem.yaml")
        """
        return import_dataitem(file, **kwargs)

    def update_dataitem(self, entity: Dataitem) -> Dataitem:
        """
        Update object. Note that object spec are immutable.

        Parameters
        ----------
        entity : Dataitem
            Object to update.

        Returns
        -------
        Dataitem
            Entity updated.

        Examples
        --------
        >>> obj = project.update_dataitem(obj)
        """
        if entity.project != self.name:
            raise ValueError(f"Entity {entity.name} is not in project {self.name}.")
        return update_dataitem(entity)

    def delete_dataitem(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        **kwargs,
    ) -> None:
        """
        Delete object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity. If True, use entity name instead of entity key as identifier.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.

        Examples
        --------
        If delete_all_versions is False:
        >>> project.delete_dataitem("store://my-dataitem-key")

        Otherwise:
        >>> project.delete_dataitem("my-dataitem-name",
        >>>                         project="my-project",
        >>>                         delete_all_versions=True)
        """
        delete_dataitem(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            delete_all_versions=delete_all_versions,
            **kwargs,
        )
        self.refresh()
