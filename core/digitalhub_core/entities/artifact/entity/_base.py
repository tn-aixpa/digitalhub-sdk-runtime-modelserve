from __future__ import annotations

import typing
from pathlib import Path
from urllib.parse import urlparse

from digitalhub_core.context.builder import get_context
from digitalhub_core.entities._base.crud import create_entity_api_ctx, read_entity_api_ctx, update_entity_api_ctx
from digitalhub_core.entities._base.entity import Entity
from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.name import build_name
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities._builders.uuid import build_uuid
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.stores.builder import get_store
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import get_timestamp
from digitalhub_core.utils.io_utils import write_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.context.context import Context
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities.artifact.spec import ArtifactSpec
    from digitalhub_core.entities.artifact.status import ArtifactStatus


class Artifact(Entity):
    """
    A class representing a artifact.

    Artifacts are (binary) objects stored in one of the artifact
    stores of the platform, and available to every process, module
    and component as files.
    """

    ENTITY_TYPE = EntityTypes.ARTIFACTS.value

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: ArtifactSpec,
        status: ArtifactStatus,
        user: str | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        project : str
            Project name.
        name : str
            Name of the object.
        uuid : str
            Version of the object.
        kind : str
            Kind the object.
        metadata : Metadata
            Metadata of the object.
        spec : ArtifactSpec
            Specification of the object.
        status : ArtifactStatus
            Status of the object.
        user : str
            Owner of the object.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.id = uuid
        self.kind = kind
        self.key = f"store://{project}/{self.ENTITY_TYPE}/{kind}/{name}:{uuid}"
        self.metadata = metadata
        self.spec = spec
        self.status = status
        self.user = user

        # Add attributes to be used in the to_dict method
        self._obj_attr.extend(["project", "name", "id", "key"])

    #############################
    #  Save / Refresh / Export
    #############################

    def save(self, update: bool = False) -> Artifact:
        """
        Save entity into backend.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        Artifact
            Entity saved.
        """
        obj = self.to_dict()

        if not update:
            new_obj = create_entity_api_ctx(self.project, self.ENTITY_TYPE, obj)
            self._update_attributes(new_obj)
            return self

        self.metadata.updated = obj["metadata"]["updated"] = get_timestamp()
        new_obj = update_entity_api_ctx(self.project, self.ENTITY_TYPE, self.id, obj)
        self._update_attributes(new_obj)
        return self

    def refresh(self) -> Artifact:
        """
        Refresh object from backend.

        Returns
        -------
        Artifact
            Entity refreshed.
        """
        new_obj = read_entity_api_ctx(self.key)
        self._update_attributes(new_obj)
        return self

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
        if filename is None:
            filename = f"{self.kind}_{self.name}_{self.id}.yml"
        pth = self._context().root / filename
        pth.parent.mkdir(parents=True, exist_ok=True)
        write_yaml(pth, obj)

    #############################
    #  Context
    #############################

    def _context(self) -> Context:
        """
        Get context.

        Returns
        -------
        Context
            Context.
        """
        return get_context(self.project)

    #############################
    #  Artifacts Methods
    #############################

    def as_file(self) -> str:
        """
        Get artifact as file. In the case of a local store, the store returns the current
        path of the artifact. In the case of a remote store, the artifact is downloaded in
        a temporary directory.

        Returns
        -------
        str
            Path of the artifact.
        """
        path = self.spec.path
        store = get_store(path)
        return store.download(path)

    def download(
        self,
        destination: str | None = None,
        force_download: bool = False,
        overwrite: bool = False,
    ) -> str:
        """
        Download artifact from storage. If store is local, the artifact is copied to
        destination path.

        Parameters
        ----------
        destination : str
            Destination path as filename.
        force_download : bool
            Force download if a previous download was already done.
        overwrite : bool
            Specify if overwrite an existing file. Default value is False.

        Returns
        -------
        str
            Path of the downloaded artifact.
        """
        path = self.spec.path
        store = get_store(path)

        if destination is None:
            filename = Path(urlparse(path).path).name
            destination = f"{self.project}/{self.ENTITY_TYPE}/{self.name}/{self.id}/{filename}"

        return store.download(path, dst=destination, force=force_download, overwrite=overwrite)

    def upload(self, source: str | None = None) -> None:
        """
        Upload artifact from given local path to spec path destination.

        Parameters
        ----------
        source : str
            Source path is the local path of the artifact.

        Returns
        -------
        None
        """
        src = source if source is not None else self.spec.src_path
        if src is None:
            raise EntityError("Source path is not specified.")

        # Upload artifact
        store = get_store(self.spec.path)
        paths = store.upload(src, self.spec.path)

        # Update file infos
        file_infos = store.get_file_info(paths)
        self._update_file_infos(file_infos)

    #############################
    #  Private Helpers
    #############################

    def _update_file_infos(self, file_infos: list[dict] | None = None) -> None:
        """
        Update file infos.

        Parameters
        ----------
        file_infos : list[dict] | None
            File infos.

        Returns
        -------
        None
        """
        if file_infos is None:
            return
        self.refresh()
        self.status.add_file(file_infos)
        self.save(update=True)

    #############################
    #  Static interface methods
    #############################

    @staticmethod
    def _parse_dict(obj: dict, validate: bool = True) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        entity : str
            Entity type.
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        project = obj.get("project")
        name = build_name(obj.get("name"))
        kind = obj.get("kind")
        uuid = build_uuid(obj.get("id"))
        metadata = build_metadata(kind, **obj.get("metadata", {}))
        spec = build_spec(kind, validate=validate, **obj.get("spec", {}))
        status = build_status(kind, **obj.get("status", {}))
        user = obj.get("user")
        return {
            "project": project,
            "name": name,
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
            "user": user,
        }
