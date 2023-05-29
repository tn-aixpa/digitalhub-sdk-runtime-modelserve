"""
Function module.
"""

from sdk.client.client import Client
from sdk.utils.utils import get_uiid
from sdk.entities.utils import file_importer, file_exporter, delete_from_backend


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


class Function:
    """
    A class representing a function.
    """

    def __init__(
        self,
        project: str,
        name: str = "",
        kind: str = "",
        source: str = "",
        image: str = "",
        tag: str = "",
        handler: str = "",
    ) -> None:
        """Initialize the Function instance."""
        self.project = project
        self.name = name
        self.kind = kind
        self.source = source
        self.image = image
        self.tag = tag
        self.handler = handler
        self.id = get_uiid()

    def save(self, client: Client, overwrite: bool = False) -> dict:
        """
        Save function into backend.

        Returns
        -------
        dict
            Mapping representaion of Function from backend.

        """
        try:
            dict_ = {
                "name": self.name,
                "project": self.project,
                "kind": self.kind,
                "spec": {
                    "source": self.source,
                    "image": self.image,
                    "tag": self.tag,
                    "handler": self.handler,
                },
            }
            return client.create_object(dict_, API_CREATE)
        except KeyError:
            raise Exception("Function already present in the backend.")

    def run(self) -> "Run": ...

    def build(self) -> "Run": ...

    def deploy(self) -> "Run": ...

    def to_dict(self) -> dict:
        """
        Return object to dict.

        Returns
        -------
        dict
            A dictionary containing the attributes of the Function instance.

        """
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __repr__(self) -> str:
        """
        Return string representation of the function object.

        Returns
        -------
        str
            A string representing the Function instance.

        """
        return str(self.to_dict())


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
    return file_importer(file, Function, OBJ_ATTR)


def export_function(function: Function, file: str) -> None:
    file_exporter(file, function.to_dict())


def get_id(key, client):
    for i in client.get_object(API_READ_ALL):
        if i["name"] == key:
            key = i["id"]
    return key
