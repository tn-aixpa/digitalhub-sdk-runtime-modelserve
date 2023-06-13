"""
Dataitem module.
"""
import pandas as pd

from sdk.entities.api import DTO_DTIT, create_api, update_api
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.utils.factories import get_context
from sdk.utils.utils import get_uiid


class DataitemMetadata(EntityMetadata):
    ...


class DataitemSpec(EntitySpec):
    def __init__(self, key: str = None, path: str = None, **kwargs) -> None:
        self.key = key
        self.path = path

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__.keys():
                self.__setattr__(k, v)


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
        uuid: str = None,
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
        self.embedded = embed
        self.id = uuid if uuid is not None else get_uiid()

        self._local = local

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set context
        self.context = get_context(self.project)

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str = None) -> dict:
        """
        Save dataitem into backend.

        Parameters
        ----------
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

        if uuid is None:
            api = create_api(self.project, DTO_DTIT)
            return self.context.client.create_object(obj, api)

        self.id = uuid
        api = update_api(self.project, DTO_DTIT, self.name, uuid)
        return self.context.client.update_object(obj, api)

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

    #############################
    #  Dataitem Methods
    #############################

    def download(self, reader) -> str:
        ...

    def upload(self, writer) -> str:
        ...

    def get_df(self, reader) -> pd.DataFrame:
        ...

    def log_df(self, writer) -> str:
        ...

    #############################
    #  Getters and Setters
    #############################

    @property
    def local(self) -> bool:
        """
        Get local flag.
        """
        return self._local

    #############################
    #  Generic Methods
    #############################

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
        uuid = d.get("id")
        if project is None or name is None:
            raise Exception("Project or name are not specified.")
        metadata = DataitemMetadata.from_dict(d.get("metadata", {"name": name}))
        spec = DataitemSpec.from_dict(d.get("spec", {}))
        return cls(project, name, metadata=metadata, spec=spec, uuid=uuid)
