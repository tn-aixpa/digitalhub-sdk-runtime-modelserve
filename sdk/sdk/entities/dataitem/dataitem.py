"""
Dataitem module.
"""
from dataclasses import dataclass

import pandas as pd

from sdk.entities.api import DTO_DTIT, create_api, update_api
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.project.context import get_context
from sdk.utils.utils import get_uiid


@dataclass
class DataitemMetadata(EntityMetadata):
    ...


@dataclass
class DataitemSpec(EntitySpec):
    key: str = None
    path: str = None


class Dataitem(Entity):
    """
    A class representing a dataitem.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str = None,
        metadata: DataitemMetadata = None,
        spec: DataitemSpec = None,
        local: bool = False,
        embed: bool = False,
        **kwargs,
    ) -> None:
        """
        Initialize the Dataitem instance.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the dataitem.
        kind : str, optional
            Kind of the dataitem, default is 'dataitem'.
        metadata : DataitemMetadata, optional
            Metadata for the dataitem, default is None.
        spec : DataitemSpec, optional
            Specification for the dataitem, default is None.
        local: bool, optional
            Specify if run locally, default is False.
        embed: bool, optional
            Specify if embed, default is False.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.kind = kind if kind is not None else "dataitem"
        self.metadata = (
            metadata if metadata is not None else DataitemMetadata(name=name)
        )
        self.spec = spec if spec is not None else DataitemSpec()
        self._local = local
        self._embed = embed

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set id if None
        if self.id is None:
            self.id = get_uiid()

        # Set context
        self.context = get_context(self.project)

    def save(self, overwrite: bool = False, uuid: str = None) -> dict:
        """
        Save dataitem into backend.

        Parameters
        ----------
        overwrite : bool, optional
            Specify if overwrite existing dataitem, default is False.
        uuid : str, optional
            Specify uuid for the dataitem to update, default is None.

        Returns
        -------
        dict
            Mapping representation of Dataitem from backend.

        """
        if self._local:
            raise Exception("Use .export() for local execution.")

        obj = self.to_dict()

        if overwrite:
            api = update_api(self.project, DTO_DTIT, uuid)
            r = self.context.client.update_object(obj, api)
        else:
            api = create_api(self.project, DTO_DTIT)
            r = self.context.client.create_object(obj, api)
        return r

    def export(self, filename: str = None) -> None:
        """
        Export object as a YAML file.

        Parameters
        ----------
        filename : str, optional
            Name of the export YAML file. If not specified, the default value is used.

        Returns
        -------
        None

        """
        obj = self.to_dict()
        filename = (
            filename
            if filename is not None
            else f"dataitem_{self.project}_{self.name}.yaml"
        )
        return self.export_object(filename, obj)

    @classmethod
    def from_dict(cls, d: dict) -> "Dataitem":
        """
        Create Dataitem instance from a dictionary.

        Parameters
        ----------
        d : dict
            Dictionary to create Dataitem from.

        Returns
        -------
        Dataitem
            Dataitem instance.

        """
        project = d.get("project")
        name = d.get("name")
        if project is None or name is None:
            raise Exception("Project or name is not specified.")
        metadata = DataitemMetadata.from_dict(d.get("metadata", {"name": name}))
        spec = DataitemSpec.from_dict(d.get("spec", {}))
        return cls(project, name, metadata=metadata, spec=spec)

    def download(self, reader) -> str:
        ...

    def upload(self, writer) -> str:
        ...

    def get_df(self, reader) -> pd.DataFrame:
        ...

    def log_df(self, writer) -> str:
        ...
