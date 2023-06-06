"""
Artifact module.
"""
from dataclasses import dataclass

from sdk.entities.api import DTO_ARTF, create_api, update_api
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.project.context import get_context
from sdk.utils.utils import get_uiid


@dataclass
class ArtifactMetadata(EntityMetadata):
    ...


@dataclass
class ArtifactSpec(EntitySpec):
    key: str = None
    source: str = None
    target_path: str = None


class Artifact(Entity):
    """
    A class representing a artifact.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str = None,
        metadata: ArtifactMetadata = None,
        spec: ArtifactSpec = None,
        local: bool = False,
        embed: bool = True,
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
        embed: bool, optional
            Specify if embed, default is False.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.kind = kind if kind is not None else "artifact"
        self.metadata = (
            metadata if metadata is not None else ArtifactMetadata(name=name)
        )
        self.spec = spec if spec is not None else ArtifactSpec()
        self._local = local
        self._embed = embed

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set id if None
        if self.id is None:
            self.id = get_uiid()

        # Set context
        self.context = get_context(self.project)

    def save(self, overwrite: bool = False, uuid: str = None) -> dict:
        """
        Save artifact into backend.

        Parameters
        ----------
        overwrite : bool, optional
            Specify if overwrite, default is False.
        uuid : str, optional
            UUID of the artifact for update, default is None.

        Returns
        -------
        dict
            Mapping representation of Artifact from backend.

        """
        if self._local:
            raise Exception("Use .export() for local execution.")

        if self._embed:
            obj = self.to_dict()
        else:
            obj = self.to_dict_not_embed()

        if overwrite:
            api = update_api(self.project, DTO_ARTF, uuid)
            r = self.context.client.update_object(obj, api)
        else:
            api = create_api(self.project, DTO_ARTF)
            r = self.context.client.create_object(obj, api)
        return r

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
        filename = (
            filename
            if filename is not None
            else f"artifact_{self.project}_{self.name}.yaml"
        )
        return self.export_object(filename, obj)

    @classmethod
    def from_dict(cls, d: dict) -> "Artifact":
        """
        Create Artifact instance from a dictionary.

        Parameters
        ----------
        d : dict
            Dictionary to create Artifact from.

        Returns
        -------
        Artifact
            Artifact instance.

        """
        project = d.get("project")
        name = d.get("name")
        if project is None or name is None:
            raise Exception("Project or name is not specified.")
        metadata = ArtifactMetadata.from_dict(d.get("metadata", {"name": name}))
        spec = ArtifactSpec.from_dict(d.get("spec", {}))
        return cls(project, name, metadata=metadata, spec=spec)

    def as_file(self, reader) -> str:
        ...

    def write_file(self):
        ...

    def upload(self, writer) -> str:
        # fare hashing
        ...
