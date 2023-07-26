"""
Artifact module.
"""
from __future__ import annotations

import typing

from sdk.entities.artifact.metadata import build_metadata
from sdk.entities.artifact.spec import build_spec
from sdk.entities.base.entity import Entity
from sdk.entities.utils.utils import get_uiid
from sdk.utils.api import DTO_ARTF, api_ctx_create, api_ctx_update
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context, get_default_store
from sdk.utils.file_utils import check_file
from sdk.utils.uri_utils import build_key, get_name_from_uri, get_uri_scheme

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
        uuid: str | None = None,
        kind: str | None = None,
        metadata: ArtifactMetadata | None = None,
        spec: ArtifactSpec | None = None,
        local: bool = False,
        embedded: bool = False,
        **kwargs,
    ) -> None:
        """
        Initialize the Artifact instance.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the object.
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        metadata : ArtifactMetadata
            Metadata of the object.
        spec : ArtifactSpec
            Specification of the object.
        local: bool
            If True, run locally.
        embedded: bool
            If True, embed object in backend.
        **kwargs
            Keyword arguments.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.id = get_uiid(uuid=uuid)
        self.kind = kind if kind is not None else "artifact"
        self.metadata = metadata if metadata is not None else build_metadata(name=name)
        self.spec = spec if spec is not None else build_spec(self.kind, **{})
        self.embedded = embedded

        # Set new attributes
        self._any_setter(**kwargs)

        # Private attributes
        self._local = local
        self._temp_path: str | None = None
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
            Path of the artifact (temporary or not).
        """
        # Get store
        store = get_default_store()

        # If local store, return local artifact path
        if store.is_local():
            # Check if source path is provided and if it is local
            src = self._parameter_or_default(None, self.spec.src_path)
            self._check_locality(src, local=True)
            return src

        # Check if target path is provided and if it is remote
        trg = self._parameter_or_default(target, self.spec.target_path)
        self._check_locality(trg)

        # Download artifact and return path
        self._temp_path = store.download(trg)
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

        # Check if target path is provided and if it is remote
        trg = self._parameter_or_default(target, self.spec.target_path)
        self._check_locality(trg)

        # Check if download destination path is specified and rebuild it if necessary
        dst = dst if dst is not None else f"./{get_name_from_uri(trg)}"

        # Check if destination path exists for overwrite
        self._check_overwrite(dst, overwrite)

        # Download artifact and return path
        store = get_default_store()
        return store.download(trg, dst)

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
        # Get store
        store = get_default_store()
        if store.is_local():
            raise EntityError("Cannot target local store for upload.")

        # Check if source path is provided and if it is local
        src = self._parameter_or_default(source, self.spec.src_path)
        self._check_locality(src, local=True)

        # Check if target path is provided and if it is remote
        if self.spec.target_path is None and target is None:
            target = f"{get_uri_scheme(store.uri)}://{build_key(src)}"
        trg = self._parameter_or_default(target, self.spec.target_path)
        self._check_locality(trg)

        # Upload artifact and return remote path
        return store.upload(src, trg)

    #############################
    #  Private Helpers
    #############################

    @staticmethod
    def _parameter_or_default(
        parameter: str | None = None, default: str | None = None
    ) -> str:
        """
        Check whether a parameter is specified or not. If not, return the default value. If also
        the default value is not specified, raise an exception. If parameter is specified, but
        default value is not, return the parameter and set the default value to the parameter.

        Parameters
        ----------
        parameter : str
            Parameter to check.
        default : str
            Default value.

        Returns
        -------
        str
            Parameter or default value.

        Raises
        ------
        EntityError
            If parameter and default value are not specified.
        """
        if parameter is None:
            if default is None:
                raise EntityError("Path is not specified.")
            return default
        return parameter

    @staticmethod
    def _check_locality(path: str, local: bool = False) -> None:
        """
        Check through URI scheme if given path is local or not.

        Parameters
        ----------
        path : str
            Path of some source.
        local : bool
            Specify if path should be local or not.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If source path is not local.
        """
        local_scheme = get_uri_scheme(path) in ["", "file"]
        if local and not local_scheme:
            raise EntityError("Only local paths are supported for source paths.")
        if not local and local_scheme:
            raise EntityError("Only remote paths are supported for target paths.")

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

        Returns
        -------
        None

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

        Returns
        -------
        bool
            Local flag.
        """
        return self._local

    @property
    def temp_path(self) -> str | None:
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
        Create object instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        Artifact
            Artifact instance.
        """
        parsed_dict = cls._parse_dict(obj)
        _obj = cls(**parsed_dict)
        _obj._local = _obj._context.local
        return _obj

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
        kind = obj.get("kind", "artifact")
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
    target_path : str
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
