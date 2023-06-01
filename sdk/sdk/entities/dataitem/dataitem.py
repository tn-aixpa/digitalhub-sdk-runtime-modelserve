"""
DataItem module.
"""
import pandas as pd

from sdk.client.client import Client
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.utils.common import API_CREATE, DTO_DTIT
from sdk.utils.utils import get_uiid


class DataItemMetadata(EntityMetadata):
    ...


class DataItemSpec(EntitySpec):
    key: str = None
    path: str = None


class DataItem(Entity):
    """
    A class representing a dataitem.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str = "dataitem",
        metadata: DataItemMetadata = None,
        spec: DataItemSpec = None,
        local: bool = False,
        **kwargs,
    ) -> None:
        """
        Initialize the DataItem instance.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the dataitem.
        kind : str, optional
            Kind of the dataitem, default is 'dataitem'.
        metadata : DataItemMetadata, optional
            Metadata for the dataitem, default is None.
        spec : DataItemSpec, optional
            Specification for the dataitem, default is None.
        local: bool, optional
            Specify if run locally, default is False.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.kind = kind
        self.metadata = metadata if metadata is not None else {}
        self.spec = spec if spec is not None else {}
        self._local = local

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set id if None
        if self.id is None:
            self.id = get_uiid()

    def save(self, client: Client, overwrite: bool = False) -> dict:
        """
        Save dataitem into backend.

        Returns
        -------
        dict
            Mapping representaion of DataItem from backend.

        """
        if self._local:
            self.export()
        api = API_CREATE.format(self.name, DTO_DTIT)
        return self.save_object(client, self.to_dict(), api, overwrite)

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
        filename = filename if filename is not None else f"dataitem_{self.name}.yaml"
        return self.export_object(filename, obj)

    def download(self, reader) -> str:
        ...

    def upload(self, writer) -> str:
        ...

    def get_df(self, reader) -> pd.DataFrame:
        ...

    def log_df(self, writer) -> str:
        ...
