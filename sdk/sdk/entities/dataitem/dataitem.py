import pandas as pd

from sdk.client.client import Client
from sdk.utils.utils import get_uiid
from sdk.entities.base_entity import Entity


class DataItem(Entity):
    """
    A class representing a dataitem.
    """

    API_CREATE = "/api/v1/dataitems"

    def __init__(
        self,
        project: str,
        key: str,
        path: str,
    ) -> None:
        """Initialize the DataItem instance."""
        self.project = project
        self.key = key
        self.path = path
        self.id = get_uiid()

    def save(self, client: Client, overwrite: bool = False) -> dict:
        """
        Save dataitem into backend.

        Returns
        -------
        dict
            Mapping representaion of DataItem from backend.

        """
        try:
            dict_ = {
                "name": self.id,
                "project": self.project,
                "kind": "job",
                "spec": {
                    "type": "dataitem",
                    "target": self.key,
                    "source": self.path,
                },
                "type": "apache-parquet",
            }
            return client.create_object(dict_, self.API_CREATE)
        except KeyError:
            raise Exception("DataItem already present in the backend.")

    def download(self, reader) -> str:
        ...

    def upload(self, writer) -> str:
        ...

    def get_df(self, reader) -> pd.DataFrame:
        ...

    def log_df(self, writer) -> str:
        ...
