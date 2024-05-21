"""
Model module.
"""
from __future__ import annotations

import typing
from pathlib import Path
from urllib.parse import urlparse

from digitalhub_core.context.builder import get_context
from digitalhub_core.entities._base.entity import Entity
from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.stores.builder import get_store
from digitalhub_core.utils.api import api_ctx_create, api_ctx_read, api_ctx_update
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import build_uuid, get_timestamp
from digitalhub_core.utils.io_utils import write_yaml
from digitalhub_core.utils.uri_utils import map_uri_scheme
from digitalhub_ml.entities.entity_types import EntityTypes

if typing.TYPE_CHECKING:
    from digitalhub_core.context.context import Context
    from digitalhub_ml.entities.models.metadata import ModelMetadata
    from digitalhub_ml.entities.models.spec import ModelSpec
    from digitalhub_ml.entities.models.status import ModelStatus


class Model(Entity):
    """
    A class representing a model.
    """

    ENTITY_TYPE = EntityTypes.MODELS.value

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: ModelMetadata,
        spec: ModelSpec,
        status: ModelStatus,
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
            Kind of the object.
        metadata : ModelMetadata
            Metadata of the object.
        spec : ModelSpec
            Specification of the object.
        status : ModelStatus
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

    def save(self, update: bool = False) -> Model:
        """
        Save entity into backend.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        Model
            Entity saved.
        """
        obj = self.to_dict()

        if not update:
            api = api_ctx_create(self.project, self.ENTITY_TYPE)
            new_obj = self._context().create_object(api, obj)
            self._update_attributes(new_obj)
            return self

        self.metadata.updated = obj["metadata"]["updated"] = get_timestamp()
        api = api_ctx_update(self.project, self.ENTITY_TYPE, self.id)
        new_obj = self._context().update_object(api, obj)
        self._update_attributes(new_obj)
        return self

    def refresh(self) -> Model:
        """
        Refresh object from backend.

        Returns
        -------
        Model
            Entity refreshed.
        """
        api = api_ctx_read(self.project, self.ENTITY_TYPE, self.id)
        obj = self._context().read_object(api)
        self._update_attributes(obj)
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
        pth = Path(self._context().project_dir) / filename
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
    #  Model methods
    #############################

    def download(
        self,
        target: str | None = None,
        destination: str | None = None,
        overwrite: bool = False,
    ) -> str:
        """
        Download model from remote storage.

        Parameters
        ----------
        target : str
            Target path is the remote path of the model
        destination : str
            Destination path as filename
        overwrite : bool
            Specify if overwrite an existing file

        Returns
        -------
        str
            Path of the downloaded model.
        """

        # Check if target path is provided and if it is remote
        trg = self._parameter_or_default(target, self.spec.path)
        self._check_remote(trg)

        # Check if download destination path is specified and rebuild it if necessary
        if destination is None:
            filename = urlparse(trg).path.split("/")[-1]
            destination = f"{self.project}/models/{self.kind}/{filename}"

        # Check if destination path exists for overwrite
        self._check_overwrite(destination, overwrite)

        # Download model and return path
        store = get_store(trg)
        return store.download(trg, destination)

    def upload(self, source: str | None = None, target: str | None = None) -> str:
        """
        Upload model to remote storage from source path to target destination.

        Parameters
        ----------
        source : str
            Source path is the local path of the model.
        target : str
            Target path is the remote path of the model.

        Returns
        -------
        str
            Path of the uploaded model.
        """
        # Check if target path is provided and if it is remote
        trg = self._parameter_or_default(target, self.spec.path)
        self._check_remote(trg)

        # Check if source path is provided and if it is local
        src = self._parameter_or_default(source, self.spec.src_path)
        self._check_local(src)

        # Get store
        store = get_store(trg)
        if store.is_local():
            raise EntityError("Cannot target local store for upload.")

        # Upload model and return remote path
        return store.upload(src, trg)

    #############################
    #  Private Helpers
    #############################

    @staticmethod
    def _parameter_or_default(parameter: str | None = None, default: str | None = None) -> str:
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
        if Path(dst).exists() and not overwrite:
            raise EntityError(f"Resource {dst} already exists.")

    #############################
    #  Static interface methods
    #############################

    @staticmethod
    def _parse_dict(obj: dict, validate: bool = True) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        project = obj.get("project")
        name = obj.get("name")
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


def model_from_parameters(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    source: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    **kwargs,
) -> Model:
    """
    Create a new Model instance with the specified parameters.

    Parameters
    ----------
    project : str
        A string representing the project associated with this model.
    name : str
        The name of the model.
    kind : str
        Kind of the object.
    uuid : str
        ID of the object in form of UUID.
    source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    description : str
        A description of the model.
    embedded : bool
        Flag to determine if object must be embedded in project.
    **kwargs
        Spec keyword arguments.

    Returns
    -------
    Model
        An instance of the created model.
    """
    uuid = build_uuid(uuid)
    metadata = build_metadata(
        kind,
        project=project,
        name=name,
        version=uuid,
        description=description,
        source=source,
        labels=labels,
        embedded=embedded,
    )
    spec = build_spec(kind, **kwargs)
    status = build_status(kind)
    return Model(
        project=project,
        name=name,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def model_from_dict(obj: dict) -> Model:
    """
    Create Model instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Model
        Model instance.
    """
    return Model.from_dict(obj, validate=False)
