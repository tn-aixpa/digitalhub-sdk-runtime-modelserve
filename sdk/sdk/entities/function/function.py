"""
Function module.
"""

from sdk.client.client import Client
from sdk.utils.utils import get_uiid
from sdk.entities.run.run import Run
from sdk.entities.base_entity import Entity
from sdk.utils.common import API_CREATE, DTO_FUNC


class Function(Entity):
    """
    A class representing a function.
    """

    def __init__(
        self,
        project: str,
        name: str,
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
        self._api_create = API_CREATE.format(self.name, DTO_FUNC)

    def save(self, client: Client, overwrite: bool = False) -> dict:
        """
        Save function into backend.

        Returns
        -------
        dict
            Mapping representaion of Function from backend.

        """
        obj = {
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
        return self.save_object(client, obj, self._api_create, overwrite)

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
        filename = filename if filename is not None else f"function_{self.name}.yaml"
        return self.export_object(filename, obj)

    def run(self) -> "Run":
        ...

    def build(self) -> "Run":
        ...

    def deploy(self) -> "Run":
        ...
