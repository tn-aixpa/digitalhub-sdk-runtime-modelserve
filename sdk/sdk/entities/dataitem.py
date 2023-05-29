"""
DataItem module.
"""
import pandas as pd

from sdk.client.client import Client
from sdk.utils.utils import get_uiid
from sdk.entities.utils import file_importer, file_exporter, delete_from_backend


API_CREATE = "/api/v1/dataitems"
API_READ = "/api/v1/dataitems/{}"
API_DELETE = "/api/v1/dataitems/{}"
API_READ_ALL = "/api/v1/dataitems"

OBJ_ATTR = ["project", "key", "path"]


class DataItem:
    """
    A class representing a dataitem.
    """

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
            return client.create_object(dict_, API_CREATE)
        except KeyError:
            raise Exception("DataItem already present in the backend.")

    def download(self, reader) -> str: ...

    def upload(self, writer) -> str: ...

    def get_df(self, reader) -> pd.DataFrame: ...

    def log_df(self, writer) -> str: ...

    def to_dict(self) -> dict:
        """
        Return object to dict.

        Returns
        -------
        dict
            A dictionary containing the attributes of the DataItem instance.

        """
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __repr__(self) -> str:
        """
        Return string representation of the dataitem object.

        Returns
        -------
        str
            A string representing the DataItem instance.

        """
        return str(self.to_dict())


def create_dataitem(
    project: str,
    key: str,
    path: str,
) -> DataItem:
    """
    Create an DataItem instance with the given parameters.
    """
    return DataItem(project, key, path)


def get_dataitem(client: Client, key: str) -> DataItem:
    """
    Retrieves dataitem details from the backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    key : str
        The key of the dataitem.

    Returns
    -------
    DataItem
        An object that contains details about the specified dataitem.

    Raises
    ------
    KeyError
        If the specified dataitem does not exist.

    """
    key = get_id(key, client)
    r = client.get_object(API_READ.format(key))
    if "status" not in r:
        kwargs = {
            "project": r.get("project"),
            "key": r.get("spec", {}).get("target"),
            "path": r.get("spec", {}).get("source"),
        }
        return DataItem(**kwargs)
    raise KeyError(f"DataItem {key} does not exists.")


def delete_dataitem(client: Client, key: str) -> None:
    """
    Delete a dataitem from backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    key : str
        The key of the dataitem.

    Returns
    -------
    None
        This function does not return anything.
    """
    api = API_DELETE.format(get_id(key, client))
    delete_from_backend(client, api)


def import_dataitem(file: str) -> DataItem:
    return file_importer(file, DataItem, OBJ_ATTR)


def export_dataitem(dataitem: DataItem, file: str) -> None:
    file_exporter(file, dataitem.to_dict())


def get_id(key, client):
    for i in client.get_object(API_READ_ALL):
        if i["spec"]["target"] == key:
            key = i["id"]
    return key
