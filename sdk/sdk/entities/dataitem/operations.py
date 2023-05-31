"""
DataItem module.
"""
from sdk.client.client import Client
from sdk.entities.utils import file_importer, file_exporter, delete_from_backend
from sdk.entities.dataitem.dataitem import DataItem
from sdk.utils.common import (
    API_READ_LATEST,
    API_READ_VERSION,
    API_DELETE_VERSION,
    API_DELETE_ALL,
    DTO_DTIT,
)


OBJ_ATTR = ["project", "key", "path"]


def new_dataitem(
    project: str,
    name: str,
    key: str = None,
    path: str = None,
    client: Client = None,
    local: bool = False,
    filename: str = None
) -> DataItem:
    """
    Create an DataItem instance with the given parameters.

    Parameters
    ----------
    project : str
        Name of the project associated with the dataitem.
    name : str
        Identifier of the dataitem.
    key : str
        Representation of artfact like store://etc..
    path : str
        Path to the dataitem on local file system or remote storage.
    client : Client, optional
        A Client object to interact with backend.
    local : bool, optional
        Flag to determine if object wil be saved locally.
    filename : str, optional
        Filename to export object.

    Returns
    -------
    DataItem
        Instance of the DataItem class representing the specified dataitem.
    """
    obj = DataItem(project, name, key, path)
    if local:
        obj.export(filename)
    else:
        obj.save(client)
    return obj


def get_dataitem(client: Client, project: str, name: str, uuid: str = None) -> DataItem:
    """
    Retrieves dataitem details from the backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    project : str
        Name of the project.
    name : str
        The name of the dataitem.
    uuid : str, optional
        UUID of dataitem specific version.

    Returns
    -------
    DataItem
        An object that contains details about the specified dataitem.

    Raises
    ------
    KeyError
        If the specified dataitem does not exist.

    """
    if uuid is not None:
        api = API_READ_VERSION.format(project, DTO_DTIT, name, uuid)
    else:
        api = API_READ_LATEST.format(project, DTO_DTIT, name)

    r = client.get_object(api)
    if "status" not in r:
        kwargs = {
            "project": r.get("project"),
            "name": r.get("name"),
            "key": r.get("spec", {}).get("target"),
            "path": r.get("spec", {}).get("source"),
        }
        return DataItem(**kwargs)
    raise KeyError(f"DataItem {name} does not exists.")


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


def delete_dataitem(client: Client, project: str, name: str, uuid: str = None) -> None:
    """
    Delete a dataitem from backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    project : str
        Name of the project.
    name : str
        The name of the dataitem.
    uuid : str, optional
        UUID of dataitem specific version.

    Returns
    -------
    None
        This function does not return anything.
    """
    if uuid is not None:
        api = API_DELETE_VERSION.format(project, DTO_DTIT, name, uuid)
    else:
        api = API_DELETE_ALL.format(project, DTO_DTIT, name)
    return delete_from_backend(client, api)

