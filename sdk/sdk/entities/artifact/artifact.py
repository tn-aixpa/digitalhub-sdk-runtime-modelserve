"""
Artifact object module.
"""

from sdk.client.client import Client
from sdk.utils.utils import get_uiid
from sdk.entities.base_entity import Entity


class Artifact(Entity):
    """
    A class representing a artifact.
    """

    API_CREATE = "/api/v1/artifacts"

    def __init__(
        self,
        project: str,
        key: str,
        path: str,
    ) -> None:
        self.project = project
        self.key = key
        self.path = path
        self.id = get_uiid()

    def save(self, client: Client, overwrite: bool = False) -> dict:
        """
        Save artifact into backend.

        Returns
        -------
        dict
            Mapping representaion of Artifact from backend.

        """
        try:
            dict_ = {
                "name": self.id,
                "project": self.project,
                "kind": "",
                "spec": {
                    "type": "artifact",
                    "target": self.key,
                    "source": self.path,
                },
                "type": "",
            }
            return client.create_object(dict_, self.API_CREATE)
        except KeyError:
            raise Exception("Artifact already present in the backend.")

    def download(self, reader) -> str:
        ...

    def upload(self, writer) -> str:
        ...
