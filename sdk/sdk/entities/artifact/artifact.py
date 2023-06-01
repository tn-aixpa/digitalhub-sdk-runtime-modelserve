"""
Artifact module.
"""
from sdk.client.client import Client
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.utils.common import API_CREATE, DTO_ARTF
from sdk.utils.utils import get_uiid


class ArtifactMetadata(EntityMetadata):
    ...


class ArtifactSpec(EntitySpec):
    key: str = None
    path: str = None


class Artifact(Entity):
    """
    A class representing a artifact.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str = "artifact",
        metadata: ArtifactMetadata = None,
        spec: ArtifactSpec = None,
        local: bool = False,
        **kwargs,
    ) -> None:
        """
        Initialize the Artifact instance.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the artifact.
        kind : str, optional
            Kind of the artifact, default is 'artifact'.
        metadata : ArtifactMetadata, optional
            Metadata for the artifact, default is None.
        spec : ArtifactSpec, optional
            Specification for the artifact, default is None.
        local: bool, optional
            Specify if run locally, default is False.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.kind = kind
        self.metadata = metadata if metadata is not None else {}
        self.spec = spec if spec is not None else {}
        self._local = local

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set id if None
        if self.id is None:
            self.id = get_uiid()

    def save(self, client: Client = None, overwrite: bool = False) -> dict:
        """
        Save artifact into backend.

        Returns
        -------
        dict
            Mapping representaion of Artifact from backend.

        """
        if self._local:
            self.export()
        api = API_CREATE.format(self.name, DTO_ARTF)
        return self.save_object(client, self.to_dict(), api, overwrite)

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
        filename = filename if filename is not None else f"artifact_{self.name}.yaml"
        return self.export_object(filename, obj)

    def as_file(self, reader) -> str:
        ...

    def write_file(self):
        ...

    def upload(self, writer) -> str:
        # fare hashing
        ...
