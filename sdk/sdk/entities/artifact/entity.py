"""
Artifact module.
"""
from __future__ import annotations

import typing
from typing import Self

from sdk.entities.artifact.metadata import build_metadata
from sdk.entities.artifact.spec import build_spec
from sdk.entities.base.entity import Entity
from sdk.entities.utils.utils import get_uiid
from sdk.utils.api import DTO_ARTF, api_ctx_create, api_ctx_update
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context, get_default_store
from sdk.utils.file_utils import check_file, get_dir
from sdk.utils.uri_utils import get_name_from_uri, get_uri_scheme, rebuild_uri

if typing.TYPE_CHECKING:
    from sdk.entities.artifact.metadata import ArtifactMetadata
    from sdk.entities.artifact.spec import ArtifactSpec


class Artifact(Entity):
    """
    A class representing a artifact.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str | None = None,
        metadata: ArtifactMetadata = None,
        spec: ArtifactSpec = None,
        local: bool = False,
        embedded: bool = False,
        uuid: str | None = None,
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
        kind : str
            Kind of the artifact
        metadata : ArtifactMetadata
            Metadata of the object.
        spec : ArtifactSpec
            Specification of the object.
        local: bool
            If True, run locally.
        embedded: bool
            If True embed object in backend.
        **kwargs
            Keyword arguments.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.kind = kind if kind is not None else "artifact"
        self.metadata = metadata if metadata is not None else build_metadata(name=name)
        self.spec = spec if spec is not None else build_spec(self.kind, **{})
        self.embedded = embedded
        self.id = uuid if uuid is not None else get_uiid()

        self._local = local

        # Temporary local artifact path (see as_file())
        self._temp_path = None

        # Set new attributes
        self._any_setter(**kwargs)

        # Set context
        self._context = get_context(self.project)

        # Set key in spec store://<project>/artifacts/<kind>/<name>:<uuid>
        self.spec.key = (
            f"store://{self.project}/artifacts/{self.kind}/{self.name}:{self.id}"
        )

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str | None = None) -> dict:
        """
        Save artifact into backend.

        Parameters
        ----------
        uuid : str
            UUID.

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
            return self._context.create_object(obj, api)

        self.id = uuid
        api = api_ctx_update(self.project, DTO_ARTF, self.name, uuid)
        return self._context.update_object(obj, api)

    def export(self, filename: str | None = None) -> None:
        """
        Export object as a YAML file.

        Parameters
        ----------
        filename : str
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

    def as_file(self, target: str | None = None) -> str:
        """
        Get artifact as file. In the case of a local store, the store returns the current
        path of the artifact. In the case of a remote store, the artifact is downloaded in
        a temporary directory.

        Parameters
        ----------
        target : str
            Target path is the remote path of the artifact where it is stored

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
        self, target: str | None = None, dst: str | None = None, overwrite: bool = False
    ) -> str:
        """
        Download artifact from backend.

        Parameters
        ----------
        target : str
            Target path is the remote path of the artifact
        dst : str
            Destination path as filename
        overwrite : bool
            Specify if overwrite an existing file

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

    def upload(self, source: str | None = None, target: str | None = None) -> str:
        """
        Upload artifact to backend.

        Parameters
        ----------
        source : str
            Source path is the local path of the artifact
        target : str
            Target path is the remote path of the artifact

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

    def _check_target(self, target: str | None = None, upload: bool = False) -> None:
        """
        Check if target path is specified.

        Parameters
        ----------
        target : str
            Target path is the remote path of the artifact

        upload : bool
            Specify if target path is for upload

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

    def _check_src(self, src: str | None = None) -> None:
        """
        Check if source path is specified.

        Parameters
        ----------
        src : str
            Source path is the local path of the artifact

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
        ignore_raise : bool
            Specify if raise an exception if target path is not remote

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

    def _rebuild_dst(self, dst: str | None = None) -> None:
        """
        Check if destination path is specified.

        Parameters
        ----------
        dst : str
            Destination path as filename

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
    def from_dict(cls, obj: dict) -> Self:
        """
        Create object instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        Self
            Self instance.
        """
        parsed_dict = cls._parse_dict(obj)
        obj_ = cls(**parsed_dict)
        obj_._local = obj_._context.local
        return obj_

    @staticmethod
    def _parse_dict(obj: dict) -> dict:
        """
        Parse dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            Parsed dictionary.
        """

        # Mandatory fields
        project = obj.get("project")
        name = obj.get("name")
        if project is None or name is None:
            raise EntityError("Project or name are not specified.")

        # Optional fields
        uuid = obj.get("id")
        kind = obj.get("kind")
        embedded = obj.get("embedded")

        # Build metadata and spec
        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(kind=kind, **spec)
        metadata = obj.get("metadata", {"name": name})
        metadata = build_metadata(**metadata)

        return {
            "project": project,
            "name": name,
            "kind": kind,
            "uuid": uuid,
            "metadata": metadata,
            "spec": spec,
            "embedded": embedded,
        }


def artifact_from_parameters(
    project: str,
    name: str,
    description: str = "",
    kind: str = "artifact",
    key: str | None = None,
    src_path: str | None = None,
    target_path: str | None = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str | None = None,
) -> Artifact:
    """
    Create artifact.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        Identifier of the artifact.
    description : str
        Description of the artifact.
    kind : str
        The type of the artifact.
    key : str
        Representation of artfact like store://etc..
    src_path : str
        Path to the artifact on local file system or remote storage.
    targeth_path : str
        Destination path of the artifact.
    local : bool
        Flag to determine if object has local execution.
    embedded : bool
        Flag to determine if object must be embedded in project.
    uuid : str
        UUID.

    Returns
    -------
    Artifact
        Artifact object.
    """
    meta = build_metadata(name=name, description=description)
    spec = build_spec(kind, key=key, src_path=src_path, target_path=target_path)
    return Artifact(
        project=project,
        name=name,
        kind=kind,
        metadata=meta,
        spec=spec,
        local=local,
        embedded=embedded,
        uuid=uuid,
    )


def artifact_from_dict(obj: dict) -> Artifact:
    """
    Create artifact from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create artifact from.

    Returns
    -------
    Artifact
        Artifact object.
    """
    return Artifact.from_dict(obj)
