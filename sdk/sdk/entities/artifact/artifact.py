"""
Artifact module.
"""
from sdk.entities.api import DTO_ARTF, create_api, update_api
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.utils.context_utils import get_context, get_store, get_default_store
from sdk.utils.utils import get_uiid
from sdk.utils.uri_utils import get_name_from_uri, rebuild_uri, get_uri_scheme
from sdk.utils.file_utils import check_file, get_dir


class ArtifactMetadata(EntityMetadata):
    ...


class ArtifactSpec(EntitySpec):
    def __init__(
        self, key: str = None, source_path: str = None, target_path: str = None, **kwargs
    ) -> None:
        self.key = key
        self.source_path = source_path
        self.target_path = target_path

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__.keys():
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
        self.embedded = embed
        self.id = uuid if uuid is not None else get_uiid()

        self._local = local

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

    def download(self, dst: str = None, overwrite: bool = False) -> str:
        """
        Download artifact from backend. If dst is None, the artifact is downloaded in the current directory.

        Parameters
        ----------
        dst : str, optional
            Destination path as filename    , default is None.
        overwrite : bool, optional
            Specify if overwrite, default is False.

        Returns
        -------
        str
            Path of the downloaded artifact.
        """
        store = get_default_store()

        if dst is None:
            filename = get_name_from_uri(self.spec.source_path)
            dst = f"./{filename}"

        if check_file(dst) and not overwrite:
            raise Exception(f"File {dst} already exists.")

        return store.fetch_artifact(self.spec.source_path, dst)

    def as_file(self) -> str:
        """
        Get artifact as file. The artifact is downloaded in a temporary directory.

        Returns
        -------
        str
            Temporary path of the artifact.
        """
        store = get_default_store()
        return store.fetch_artifact(self.spec.source_path)

    def upload(self) -> str:
        """
        Upload artifact to backend.

        Returns
        -------
        str
            Path of the uploaded artifact.
        """
        # TODO: hashing of the file
        store = get_default_store()

        # Check if source path is local
        if get_uri_scheme(self.src_pth) not in ["", "file"]:
            raise Exception(
                "Only local source paths are supported for upload."
            )

        # Check if target path is provided.
        # Rebuild if not provided and update spec.
        if self.trg_pth is None:
            path = get_dir(self.src_pth)
            filename = get_name_from_uri(self.src_pth)
            target_path = rebuild_uri(f"{path}/{filename}")
            target_uri = store.persist_artifact(self.src_pth, target_path)

            # Update target path
            self.spec.target_path = target_uri
            return self.trg_pth

        return store.persist_artifact(self.src_pth, self.trg_pth)

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
    def src_pth(self) -> str:
        """
        Get source path of the artifact from spec.

        Returns
        -------
        str
            Source path of the artifact.
        """
        return self.spec.source_path

    @property
    def trg_pth(self) -> str:
        """
        Get target path of the artifact from spec.

        Returns
        -------
        str
            Destination path of the artifact.
        """
        return self.spec.target_path

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
