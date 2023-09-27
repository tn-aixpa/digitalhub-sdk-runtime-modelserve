"""
Artifact module.
"""
from __future__ import annotations

import typing

from sdk.context.factory import get_context
from sdk.entities.base.entity import Entity
from sdk.entities.builders.kinds import build_kind
from sdk.entities.builders.metadata import build_metadata
from sdk.entities.builders.spec import build_spec
from sdk.entities.builders.status import build_status
from sdk.store.factory import get_store
from sdk.utils.api import api_ctx_create, api_ctx_update
from sdk.utils.commons import ARTF
from sdk.utils.exceptions import EntityError
from sdk.utils.file_utils import check_file
from sdk.utils.generic_utils import get_uiid
from sdk.utils.uri_utils import get_name_from_uri, map_uri_scheme

if typing.TYPE_CHECKING:
    from sdk.entities.artifact.spec.objects.base import ArtifactSpec
    from sdk.entities.base.metadata import Metadata
    from sdk.entities.base.status import Status


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
        metadata: Metadata | None = None,
        spec: ArtifactSpec | None = None,
        status: Status | None = None,
        local: bool = False,
        embedded: bool = True,
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
        metadata : Metadata
            Metadata of the object.
        spec : ArtifactSpec
            Specification of the object.
        status : Status
            State of the object.
        local: bool
            If True, export locally.
        embedded: bool
            If True, embed object in backend.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.id = get_uiid(uuid=uuid)
        self.kind = kind if kind is not None else build_kind(ARTF)
        self.metadata = metadata if metadata is not None else build_metadata(name=name)
        self.spec = spec if spec is not None else build_spec(ARTF, self.kind, **{})
        self.status = status if status is not None else build_status()
        self.embedded = embedded

        # Private attributes
        self._local = local
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
            api = api_ctx_create(self.project, ARTF)
            return self._context.create_object(obj, api)

        self.id = uuid
        api = api_ctx_update(self.project, ARTF, self.name, uuid)
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
        # Check if target path is provided and if it is remote
        trg = self._parameter_or_default(target, self.spec.target_path)
        self._check_remote(trg)

        # If local store, return local artifact path
        # Check if source path is provided and if it is local
        store = get_store(trg)
        if store.is_local():
            src = self._parameter_or_default(None, self.spec.src_path)
            self._check_local(src)
            return src

        return store.download(trg)

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
        self._check_remote(trg)

        # Check if download destination path is specified and rebuild it if necessary
        dst = dst if dst is not None else f"./{get_name_from_uri(trg)}"

        # Check if destination path exists for overwrite
        self._check_overwrite(dst, overwrite)

        # Download artifact and return path
        store = get_store(trg)
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
        # Check if target path is provided and if it is remote
        trg = self._parameter_or_default(target, self.spec.target_path)
        self._check_remote(trg)

        # Check if source path is provided and if it is local
        src = self._parameter_or_default(source, self.spec.src_path)
        self._check_local(src)

        # Get store
        store = get_store(trg)
        if store.is_local():
            raise EntityError("Cannot target local store for upload.")

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
    def _check_local(path: str) -> None:
        """
        Check through URI scheme if given path is local or not.

        Parameters
        ----------
        path : str
            Path of some source.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If source path is not local.
        """
        if map_uri_scheme(path) != "local":
            raise EntityError("Only local paths are supported for source paths.")

    @staticmethod
    def _check_remote(path: str) -> None:
        """
        Check through URI scheme if given path is remote.

        Parameters
        ----------
        path : str
            Path of some source.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If source path is local.
        """
        if map_uri_scheme(path) == "local":
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
        kind = obj.get("kind")
        kind = build_kind(ARTF, obj.get("kind"))
        embedded = obj.get("embedded")

        # Build metadata, spec, status
        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(ARTF, kind=kind, **spec)
        metadata = obj.get("metadata", {"name": name})
        metadata = build_metadata(**metadata)
        status = obj.get("status")
        status = status if status is not None else {}
        status = build_status(**status)

        return {
            "project": project,
            "name": name,
            "kind": kind,
            "uuid": uuid,
            "metadata": metadata,
            "spec": spec,
            "status": status,
            "embedded": embedded,
        }


def artifact_from_parameters(
    project: str,
    name: str,
    description: str = "",
    kind: str | None = None,
    key: str | None = None,
    src_path: str | None = None,
    target_path: str | None = None,
    local: bool = False,
    embedded: bool = True,
    uuid: str | None = None,
    **kwargs,
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
        Path to the artifact on local file system.
    target_path : str
        Destination path of the artifact.
    local : bool
        Flag to determine if object will be exported to backend.
    embedded : bool
        Flag to determine if object must be embedded in project.
    uuid : str
        UUID.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Artifact
        Artifact object.
    """
    kind = build_kind(ARTF, kind)
    spec = build_spec(
        ARTF, kind, key=key, src_path=src_path, target_path=target_path, **kwargs
    )
    meta = build_metadata(name=name, description=description)
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
