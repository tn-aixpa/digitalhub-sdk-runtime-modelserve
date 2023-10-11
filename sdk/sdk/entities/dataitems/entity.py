"""
Dataitem module.
"""
from __future__ import annotations

import typing

from sdk.context.builder import get_context
from sdk.entities.base.entity import Entity
from sdk.entities.builders.kinds import build_kind
from sdk.entities.builders.metadata import build_metadata
from sdk.entities.builders.spec import build_spec
from sdk.entities.builders.status import build_status
from sdk.stores.builder import get_default_store, get_store
from sdk.utils.api import api_ctx_create, api_ctx_update
from sdk.utils.commons import DTIT
from sdk.utils.exceptions import EntityError
from sdk.utils.file_utils import clean_all, get_dir
from sdk.utils.generic_utils import build_uuid, get_timestamp
from sdk.utils.uri_utils import get_extension, map_uri_scheme

if typing.TYPE_CHECKING:
    import pandas as pd

    from sdk.context.context import Context
    from sdk.entities.dataitems.metadata import DataitemMetadata
    from sdk.entities.dataitems.spec.objects.base import DataitemSpec
    from sdk.entities.dataitems.status import DataitemStatus


class Dataitem(Entity):
    """
    A class representing a dataitem.
    """

    def __init__(
        self,
        uuid: str,
        kind: str,
        metadata: DataitemMetadata,
        spec: DataitemSpec,
        status: DataitemStatus,
    ) -> None:
        """
        Initialize the Dataitem instance.

        Parameters
        ----------
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        metadata : DataitemMetadata
            Metadata of the object.
        spec : DataitemSpec
            Specification of the object.
        status : DataitemStatus
            State of the object.
        """
        super().__init__()
        self.id = uuid
        self.kind = kind
        self.metadata = metadata
        self.spec = spec
        self.status = status

        self.project = self.metadata.project
        self.name = self.metadata.name
        self.embedded = self.metadata.embedded
        self._obj_attr.extend(["project", "name", "embedded"])

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str | None = None) -> dict:
        """
        Save dataitem into backend.

        Parameters
        ----------
        uuid : str
            Specify uuid for the dataitem to update

        Returns
        -------
        dict
            Mapping representation of Dataitem from backend.
        """
        obj = self.to_dict()

        if uuid is None:
            api = api_ctx_create(self.metadata.project, DTIT)
            return self._context().create_object(obj, api)

        self.id = uuid
        self.metadata.updated = get_timestamp()
        obj["metadata"]["updated"] = self.metadata.updated
        api = api_ctx_update(self.metadata.project, DTIT, self.metadata.name, uuid)
        return self._context().update_object(obj, api)

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
            else f"dataitem_{self.metadata.project}_{self.metadata.name}.yaml"
        )
        self._export_object(filename, obj)

    #############################
    #  Dataitem Methods
    #############################

    def as_df(self, file_format: str | None = None, **kwargs) -> pd.DataFrame:
        """
        Read dataitem as a pandas DataFrame. If the dataitem is not local, it will be downloaded
        to a temporary folder and deleted after the method is executed. If no file_format is passed,
        the function will try to infer it from the dataitem.spec.path attribute.
        The path of the dataitem is specified in the spec attribute, and must be a store aware path.
        If the dataitem is stored on an s3 bucket, the path must be s3://<bucket>/<path_to_dataitem>.
        If the dataitem is stored on a database (Postgres is the only one supported), the path must
        be sql://postgres/<database>/<schema>/<table/view>.

        Parameters
        ----------
        file_format : str
            Format of the file. (Supported csv and parquet).
        **kwargs
            Keyword arguments.

        Returns
        -------
        pd.DataFrame
            Pandas DataFrame.
        """
        if self.spec.path is None:
            raise EntityError("Path is not specified.")

        store = get_store(self.spec.path)
        tmp_path = False

        # Check file format
        extension = self._get_extension(self.spec.path, file_format)

        # Download dataitem if not local
        if not self._check_local(self.spec.path):
            path = store.download(self.spec.path)
            tmp_path = True
        else:
            path = self.spec.path

        df = store.read_df(path, extension, **kwargs)
        if tmp_path:
            clean_all(get_dir(path))

        return df

    def write_df(
        self, target_path: str | None = None, df: pd.DataFrame | None = None, **kwargs
    ) -> str:
        """
        Write pandas DataFrame as parquet.
        If no target_path is passed, the dataitem will be written into the default store.
        If no DataFrame is passed, the dataitem will be written into the target_path.

        Parameters
        ----------
        target_path : str
            Path to write the dataframe to
        df : pd.DataFrame
            DataFrame to write.
        **kwargs
            Keyword arguments.

        Returns
        -------
        str
            Path to the written dataframe.
        """
        if target_path is None:
            store = get_default_store()
        else:
            store = get_store(target_path)
        if df is None:
            df = self.as_df()
        return store.write_df(df, target_path, **kwargs)

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
        return get_context(self.metadata.project)

    #############################
    #  Helper Methods
    #############################

    @staticmethod
    def _check_local(path: str) -> bool:
        """
        Check if path is local.

        Parameters
        ----------
        path : str
            Path to check.

        Returns
        -------
        bool
            True if local, False otherwise.
        """
        return map_uri_scheme(path) == "local"

    @staticmethod
    def _get_extension(path: str, file_format: str | None = None) -> str:
        """
        Get extension of path.

        Parameters
        ----------
        path : str
            Path to get extension from.
        file_format : str
            File format.

        Returns
        -------
        str
            File extension.

        Raises
        ------
        EntityError
            If file format is not supported.
        """
        if file_format is not None:
            return file_format
        scheme = map_uri_scheme(path)
        if scheme == "sql":
            return "parquet"
        ext = get_extension(path)
        if ext is None:
            raise EntityError(
                "Unknown file format. Only csv and parquet are supported."
            )
        return ext

    #############################
    #  Generic Methods
    #############################

    @classmethod
    def from_dict(cls, obj: dict) -> "Dataitem":
        """
        Create object instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        Dataitem
            Dataitem instance.
        """
        parsed_dict = cls._parse_dict(obj)
        return cls(**parsed_dict)

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

        # Build UUID, kind, metadata, spec and status
        uuid = obj.get("id")
        uuid = build_uuid(uuid)

        kind = obj.get("kind")
        kind = build_kind(DTIT, kind)

        metadata = obj.get("metadata")
        metadata = (
            metadata
            if metadata is not None
            else {"project": project, "name": name, "version": uuid}
        )
        metadata = build_metadata(DTIT, **metadata)

        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(DTIT, kind=kind, **spec)

        status = obj.get("status")
        status = status if status is not None else {}
        status = build_status(DTIT, **status)

        return {
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
        }


def dataitem_from_parameters(
    project: str,
    name: str,
    description: str | None = None,
    kind: str | None = None,
    key: str | None = None,
    path: str | None = None,
    embedded: bool = True,
    uuid: str | None = None,
    **kwargs,
) -> Dataitem:
    """
    Create a new object instance.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        Identifier of the dataitem.
    description : str
        Description of the dataitem.
    kind : str
        The type of the dataitem.
    key : str
        Representation of the dataitem, e.g. store://etc.
    path : str
        Path to the dataitem on local file system or remote storage.
    embedded : bool
        Flag to determine if object must be embedded in project.
    uuid : str
        UUID.
    **kwargs

    Returns
    -------
    Dataitem
        Dataitem object.
    """
    uuid = build_uuid(uuid)
    kind = build_kind(DTIT, kind)
    key = (
        key if key is not None else f"store://{project}/dataitems/{kind}/{name}:{uuid}"
    )
    metadata = build_metadata(
        DTIT,
        project=project,
        name=name,
        version=uuid,
        description=description,
        embedded=embedded,
    )
    spec = build_spec(
        DTIT,
        kind,
        key=key,
        path=path,
        **kwargs,
    )
    status = build_status(DTIT)
    return Dataitem(
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def dataitem_from_dict(obj: dict) -> Dataitem:
    """
    Create dataitem from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create dataitem from.

    Returns
    -------
    Dataitem
        Dataitem object.
    """
    return Dataitem.from_dict(obj)
