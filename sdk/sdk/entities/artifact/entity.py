"""
Artifact module.
"""
from sdk.utils.api import DTO_ARTF, api_ctx_create, api_ctx_update
from sdk.entities.base.entity import Entity, EntityMetadata, EntitySpec
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context, get_default_store
from sdk.utils.file_utils import check_file, get_dir
from sdk.utils.uri_utils import (
    get_name_from_uri,
    get_uri_scheme,
    rebuild_uri,
)
from sdk.utils.utils import get_uiid


class ArtifactMetadata(EntityMetadata):
    """
    Artifact metadata.
    """


class ArtifactSpec(EntitySpec):
    """
    Artifact specification.
    """

    def __init__(
        self,
        key: str = None,
        src_path: str = None,
        target_path: str = None,
        **kwargs,
    ) -> None:
        self.key = key
        self.src_path = src_path
        self.target_path = target_path

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__:
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

        # Temporary local artifact path (see as_file())
        self._temp_path = None

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set context
        self.context = get_context(self.project)

        # Set key in spec store://<project>/artifacts/<kind>/<name>:<uuid>
        self.spec.key = (
            f"store://{self.project}/artifacts/{self.kind}/{self.name}:{self.id}"
        )

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
            raise EntityError("Use .export() for local execution.")

        obj = self.to_dict()

        if uuid is None:
            api = api_ctx_create(self.project, DTO_ARTF)
            return self.context.client.create_object(obj, api)

        self.id = uuid
        api = api_ctx_update(self.project, DTO_ARTF, self.name, uuid)
        return self.context.client.update_object(obj, api)

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
        self._export_object(filename, obj)

    #############################
    #  Artifacts Methods
    #############################

    def as_file(self, target: str = None) -> str:
        """
        Get artifact as file. In the case of a local store, the store returns the current
        path of the artifact. In the case of a remote store, the artifact is downloaded in
        a temporary directory.

        Parameters
        ----------
        target : str, optional
            Target path is the remote path of the artifact where it is stored, default is None.

        Returns
        -------
        str
            Temporary path of the artifact.
        """
        # Get store
        store = get_default_store()

        # If local store, return local artifact path
        if store.is_local():
            self._check_src()
            return self.spec.src_path

        # Check if target path is specified
        self._check_target(target)

        # Check if target path is remote
        self._check_remote()

        # Download artifact and return path
        self._temp_path = store.download(self.spec.target_path)
        return self._temp_path

    def download(
        self, target: str = None, dst: str = None, overwrite: bool = False
    ) -> str:
        """
        Download artifact from backend.

        Parameters
        ----------
        target : str, optional
            Target path is the remote path of the artifact, default is None.
        dst : str, optional
            Destination path as filename, default is None.
        overwrite : bool, optional
            Specify if overwrite an existing file, default is False.

        Returns
        -------
        str
            Path of the downloaded artifact.
        """

        # Check if target path is specified
        self._check_target(target)

        # Check if target path is remote
        self._check_remote()

        # Check if download destination path is specified and rebuild it if necessary
        dst = self._rebuild_dst(dst)

        # Check if destination path exists for overwrite
        self._check_overwrite(dst, overwrite)

        # Get store
        store = get_default_store()

        # Download artifact and return path
        return store.download(self.spec.target_path, dst)

    def upload(self, source: str = None, target: str = None) -> str:
        """
        Upload artifact to backend.

        Parameters
        ----------
        source : str, optional
            Source path is the local path of the artifact, default is None.
        target : str, optional
            Target path is the remote path of the artifact, default is None.

        Returns
        -------
        str
            Path of the uploaded artifact.
        """
        # Check if source path is provided.
        self._check_src(source)

        # Check if source path is local
        self._check_local()

        # Check if target path is provided.
        self._check_target(target, upload=True)

        # Check if target path is remote
        self._check_remote()

        # Get store
        store = get_default_store()

        # Upload artifact and return remote path
        return store.upload(self.spec.src_path, self.spec.target_path)

    #############################
    #  Private Helpers
    #############################

    def _check_target(self, target: str = None, upload: bool = False) -> None:
        """
        Check if target path is specified.

        Parameters
        ----------
        target : str, optional
            Target path is the remote path of the artifact, default is None.

        upload : bool, optional
            Specify if target path is for upload, default is False.

        Returns
        -------
        None

        """
        if self.spec.target_path is None:
            if target is None:
                if not upload:
                    raise EntityError("Target path is not specified.")
                path = get_dir(self.spec.src_path)
                filename = get_name_from_uri(self.spec.src_path)
                target_path = rebuild_uri(f"{path}/{filename}")
                self.spec.target_path = target_path
                return
            self.spec.target_path = target
            return

    def _check_src(self, src: str = None) -> None:
        """
        Check if source path is specified.

        Parameters
        ----------
        src : str, optional
            Source path is the local path of the artifact, default is None.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If source path is not specified.
        """
        if self.spec.src_path is None:
            if src is None:
                raise EntityError("Source path is not specified.")
            self.spec.src_path = src

    def _check_remote(self) -> None:
        """
        Check if target path is remote.

        Parameters
        ----------
        ignore_raise : bool, optional
            Specify if raise an exception if target path is not remote, default is True.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If target path is not remote.
        """
        if self.spec.target_path is None:
            return
        if get_uri_scheme(self.spec.target_path) in ["", "file"]:
            raise EntityError("Only remote source URIs are supported for target paths")

    def _check_local(self) -> None:
        """
        Check if source path is local.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If source path is not local.
        """
        if get_uri_scheme(self.spec.src_path) not in ["", "file"]:
            raise EntityError("Only local paths are supported for source paths.")

    def _rebuild_dst(self, dst: str = None) -> None:
        """
        Check if destination path is specified.

        Parameters
        ----------
        dst : str, optional
            Destination path as filename, default is None.

        Returns
        -------
        str
            Destination path as filename.
        """
        if dst is None:
            dst = f"./{get_name_from_uri(self.spec.target_path)}"
        return dst

    @staticmethod
    def _check_overwrite(dst: str, overwrite: bool) -> None:
        """
        Check if destination path exists for overwrite.

        Parameters
        ----------
        dst : str
            Destination path as filename.
        overwrite : bool
            Specify if overwrite an existing file.

        Raises
        ------
        Exception
            If destination path exists and overwrite is False.
        """
        if check_file(dst) and not overwrite:
            raise EntityError(f"File {dst} already exists.")

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
    def temp_path(self) -> str:
        """
        Get temporary path.
        """
        return self._temp_path

    #############################
    #  Generic Methods
    #############################

    @classmethod
    def from_dict(cls, obj: dict) -> "Artifact":
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
        project = obj.get("project")
        name = obj.get("name")
        uuid = obj.get("id")
        if project is None or name is None:
            raise EntityError("Project or name are not specified.")
        metadata = ArtifactMetadata.from_dict(obj.get("metadata", {"name": name}))
        spec = ArtifactSpec.from_dict(obj.get("spec", {}))
        return cls(project, name, metadata=metadata, spec=spec, uuid=uuid)
