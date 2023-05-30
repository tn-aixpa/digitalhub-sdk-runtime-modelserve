from sdk.client.client import Client
from sdk.entities.utils import file_importer, file_exporter, delete_from_backend
from sdk.entities.function.function import Function


API_CREATE = "/api/v1/functions"
API_READ = "/api/v1/functions/{}"
API_DELETE = "/api/v1/functions/{}"
API_READ_ALL = "/api/v1/functions"

OBJ_ATTR = [
    "project",
    "name",
    "kind",
    "source",
    "image",
    "tag",
    "handler",
]


def create_function(
    project: str,
    name: str = None,
    kind: str = None,
    source: str = None,
    image: str = None,
    tag: str = None,
    handler: str = None,
) -> Function:
    """
    Create a Function instance with the given parameters.
    """
    return Function(project, name, kind, source, image, tag, handler)


def get_function(client: Client, name: str) -> Function:
    """
    Retrieves function details from the backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    name : str
        The name of the function.

    Returns
    -------
    Function
        An object that contains details about the specified function.

    Raises
    ------
    KeyError
        If the specified function does not exist.

    """
    key = get_id(name, client)
    r = client.get_object(API_READ.format(key))
    if "status" not in r:
        kwargs = {
            "project": r.get("project"),
            "kind": r.get("kind"),
            "name": r.get("name"),
            "source": r.get("spec", {}).get("source"),
            "image": r.get("spec", {}).get("image"),
            "tag": r.get("spec", {}).get("tag"),
            "handler": r.get("spec", {}).get("handler"),
        }
        return Function(**kwargs)
    raise KeyError(f"Function {key} does not exists.")


def delete_function(client: Client, name: str) -> None:
    """
    Delete a function.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    name : str
        The name of the function.

    Returns
    -------
    None
        This function does not return anything.
    """
    api = API_DELETE.format(get_id(name, client))
    delete_from_backend(client, api)


def import_function(file: str) -> Function:
    """
    Import an Function object from a file using the specified file path.

    Parameters
    ----------
    file : str
        The absolute or relative path to the file containing the Function object.

    Returns
    -------
    Function
        The Function object imported from the file using the specified path.

    """
    return file_importer(file, Function, OBJ_ATTR)


def export_function(function: Function, file: str) -> None:
    """
    Export the specified Function object to a file in the specified location.

    Parameters
    ----------
    function : Function
        The Function object to be exported.
    file : str
        The absolute or relative path to the file in which the Function object
        will be exported.

    Returns
    -------
    None
    """
    file_exporter(file, function.to_dict())


def get_id(key, client):
    for i in client.get_object(API_READ_ALL):
        if i["name"] == key:
            key = i["id"]
    return key
