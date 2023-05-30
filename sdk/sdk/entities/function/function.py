"""
Function module.
"""

from sdk.client.client import Client
from sdk.utils.utils import get_uiid
from sdk.entities.run.run import Run


class Function:
    """
    A class representing a function.
    """

    API_CREATE = "/api/v1/functions"

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
            return client.create_object(dict_, self.API_CREATE)
        except KeyError:
            raise Exception("Function already present in the backend.")

    def run(self) -> "Run":
        ...

    def build(self) -> "Run":
        ...

    def deploy(self) -> "Run":
        ...

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
