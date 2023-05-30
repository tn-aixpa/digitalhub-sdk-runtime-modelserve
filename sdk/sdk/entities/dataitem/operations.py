"""
DataItem module.
"""
from sdk.client.client import Client
from sdk.entities.utils import file_importer, file_exporter, delete_from_backend
from sdk.entities.dataitem.dataitem import DataItem


API_CREATE = "/api/v1/dataitems"
API_READ = "/api/v1/dataitems/{}"
API_DELETE = "/api/v1/dataitems/{}"
API_READ_ALL = "/api/v1/dataitems"

OBJ_ATTR = ["project", "key", "path"]


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
    """
    Import an DataItem object from a file using the specified file path.

    Parameters
    ----------
    file : str
        The absolute or relative path to the file containing the DataItem object.

    Returns
    -------
    DataItem
        The DataItem object imported from the file using the specified path.

    """
    return file_importer(file, DataItem, OBJ_ATTR)


def export_dataitem(dataitem: DataItem, file: str) -> None:
    """
    Export the specified DataItem object to a file in the specified location.

    Parameters
    ----------
    dataitem : DataItem
        The DataItem object to be exported.
    file : str
        The absolute or relative path to the file in which the DataItem object
        will be exported.

    Returns
    -------
    None
    """
    file_exporter(file, dataitem.to_dict())


def get_id(key, client):
    for i in client.get_object(API_READ_ALL):
        if i["spec"]["target"] == key:
            key = i["id"]
    return key
