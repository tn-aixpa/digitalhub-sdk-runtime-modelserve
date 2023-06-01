"""
DataItem module.
"""
from sdk.client.factory import get_client
from sdk.entities.utils import file_importer
from sdk.entities.dataitem.dataitem import DataItem, DataItemMetadata, DataItemSpec
from sdk.utils.api import (
    API_READ_LATEST,
    API_READ_VERSION,
    API_DELETE_VERSION,
    API_DELETE_ALL,
    DTO_DTIT,
)


def new_dataitem(
    project: str,
    name: str,
    description: str = None,
    kind: str = None,
    key: str = None,
    path: str = None,
    local: bool = False,
    filename: str = None,
) -> DataItem:
    """
    Create an DataItem instance with the given parameters.

    Parameters
    ----------
    project : str
        Name of the project associated with the dataitem.
    name : str
        Identifier of the dataitem.
    description : str, optional
        Description of the dataitem.
    kind : str, optional
        The type of the dataitem.
    key : str
        Representation of artfact like store://etc..
    path : str
        Path to the dataitem on local file system or remote storage.
    local : bool, optional
        Flag to determine if object will be saved locally.

    Returns
    -------
    DataItem
        Instance of the DataItem class representing the specified dataitem.
    """
    meta = DataItemMetadata(name=name, description=description)
    spec = DataItemSpec(key=key, path=path)
    obj = DataItem(project, name, kind, meta, spec)
    if not local:
        obj.save()
    return obj


def get_dataitem(project: str, name: str, uuid: str = None) -> DataItem:
    """
    Retrieves dataitem details from the backend.

    Parameters
    ----------
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
    client = get_client()
    r = client.get_object(api)
    if "status" not in r:
        return DataItem(**r)
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
    return file_importer(file, DataItem)


def delete_dataitem(project: str, name: str, uuid: str = None) -> None:
    """
    Delete a dataitem from backend.

    Parameters
    ----------
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
    client = get_client()
    if uuid is not None:
        api = API_DELETE_VERSION.format(project, DTO_DTIT, name, uuid)
    else:
        api = API_DELETE_ALL.format(project, DTO_DTIT, name)
    return client.delete_object(api)
