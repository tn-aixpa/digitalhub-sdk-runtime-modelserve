"""
Artifact module.
"""
from sdk.entities.api import DTO_ARTF, create_api, update_api
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.utils.context_utils import get_context
from sdk.utils.utils import get_uiid


class ArtifactMetadata(EntityMetadata):
    ...


class ArtifactSpec(EntitySpec):
    def __init__(
        self, key: str = None, source: str = None, target_path: str = None, **kwargs
    ) -> None:
        self.key = key
        self.source = source
        self.target_path = target_path

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.get_sig():
                self.__setattr__(k, v)


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
        embed: bool = False,
        uuid: str = None,
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
        self.id = uuid if uuid is not None else get_uiid()

        self._local = local
        self._embed = embed

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set context
        self.context = get_context(self.project)

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str = None) -> dict:
        """
        Save artifact into backend.

        Parameters
        ----------
        uuid : str, optional
            UUID of the artifact for update, default is None.

        Returns
        -------
        dict
            Mapping representation of Artifact from backend.

        """
        if self._local:
            raise Exception("Use .export() for local execution.")

        obj = self.to_dict()

        if uuid is not None:
            self.id = uuid
            try:
                api = update_api(self.project, DTO_ARTF, uuid)
                return self.context.client.update_object(obj, api)
            except Exception:
                ...
        api = create_api(self.project, DTO_ARTF)
        return self.context.client.create_object(obj, api)

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

    #############################
    #  Artifacts Methods
    #############################

    def as_file(self, reader) -> str:
        ...

    def write_file(self):
        ...

    def upload(self, writer) -> str:
        # fare hashing
        ...

    #############################
    #  Getters and Setters
    #############################

    @property
    def local(self) -> bool:
        """
        Get local flag.
        """
        return self._local

    @property
    def embed(self) -> bool:
        """
        Get embed flag.
        """
        return self._embed

    #############################
    #  Generic Methods
    #############################

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
        uuid = d.get("id")
        if project is None or name is None:
            raise Exception("Project or name are not specified.")
        metadata = ArtifactMetadata.from_dict(d.get("metadata", {"name": name}))
        spec = ArtifactSpec.from_dict(d.get("spec", {}))
        return cls(project, name, metadata=metadata, spec=spec, uuid=uuid)
