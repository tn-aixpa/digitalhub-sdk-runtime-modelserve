"""
Workflow module.
"""

from sdk.client.client import Client
from sdk.utils.utils import get_uiid
from sdk.entities.run.run import Run
from sdk.entities.base_entity import Entity


class Workflow(Entity):
    """
    A class representing a workflow.
    """

    API_CREATE = "/api/v1/workflows"

    def __init__(
        self, project: str, name: str = None, kind: str = None, spec: dict = None
    ) -> None:
        """Initialize the Workflow instance."""
        self.project = project
        self.name = name
        self.kind = kind
        self.spec = spec if spec is not None else {}
        self.id = get_uiid()

    def save(self, client: Client, overwrite: bool = False) -> dict:
        """
        Save workflow into backend.

        Returns
        -------
        dict
            Mapping representaion of Workflow from backend.

        """
        try:
            dict_ = {
                "name": self.name,
                "project": self.project,
                "kind": self.kind,
                "spec": self.spec,
            }
            return client.create_object(dict_, self.API_CREATE)
        except KeyError:
            raise Exception("Workflow already present in the backend.")

    def run(self) -> "Run":
        ...

    def schedule(self) -> "Run":
        ...
