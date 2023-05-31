"""
Workflow module.
"""

from sdk.client.client import Client
from sdk.utils.utils import get_uiid
from sdk.entities.run.run import Run
from sdk.entities.base_entity import Entity
from sdk.utils.common import API_CREATE, DTO_WKFL


class Workflow(Entity):
    """
    A class representing a workflow.
    """

    def __init__(
        self, project: str, name: str = None, kind: str = None, spec: dict = None
    ) -> None:
        """Initialize the Workflow instance."""
        self.project = project
        self.name = name
        self.kind = kind
        self.spec = spec if spec is not None else {}
        self.id = get_uiid()
        self._api_create = API_CREATE.format(self.name, DTO_WKFL)

    def save(self, client: Client, overwrite: bool = False) -> dict:
        """
        Save workflow into backend.

        Returns
        -------
        dict
            Mapping representaion of Workflow from backend.

        """
        obj = {
            "name": self.name,
            "project": self.project,
            "kind": self.kind,
            "spec": self.spec,
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
        filename = filename if filename is not None else f"workflow_{self.name}.yaml"
        return self.export_object(filename, obj)

    def run(self) -> "Run":
        ...

    def schedule(self) -> "Run":
        ...
