"""
Dataitem module.
"""
from __future__ import annotations

import typing
from typing import Self

from sdk.entities.base.entity import Entity
from sdk.entities.dataitem.metadata import build_metadata
from sdk.entities.dataitem.spec import build_spec
from sdk.entities.utils.utils import get_uiid
from sdk.utils.api import DTO_DTIT, api_ctx_create, api_ctx_update
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context, get_default_store
from sdk.utils.file_utils import check_file, clean_all, get_dir
from sdk.utils.uri_utils import get_extension, get_uri_scheme

if typing.TYPE_CHECKING:
    import pandas as pd

    from sdk.entities.dataitem.metadata import DataitemMetadata
    from sdk.entities.dataitem.spec import DataitemSpec


class Dataitem(Entity):
    """
    A class representing a dataitem.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str = None,
        metadata: DataitemMetadata = None,
        spec: DataitemSpec = None,
        local: bool = False,
        embedded: bool = False,
        uuid: str = None,
        **kwargs,
    ) -> None:
        """
        Initialize the Dataitem instance.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the dataitem.
        kind : str
            Kind of the dataitem
        metadata : DataitemMetadata
            Metadata of the object.
        spec : DataitemSpec
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
        self.kind = kind if kind is not None else "dataitem"
        self.metadata = (
            metadata if metadata is not None else DataitemMetadata(name=name)
        )
        self.spec = spec if spec is not None else DataitemSpec()
        self.embedded = embedded
        self.id = uuid if uuid is not None else get_uiid()

        self._local = local

        # Set new attributes
        self._any_setter(**kwargs)

        # Set context
        self._context = get_context(self.project)

        # Set key in spec store://<project>/dataitems/<kind>/<name>:<uuid>
        self.spec.key = (
            f"store://{self.project}/dataitems/{self.kind}/{self.name}:{self.id}"
        )

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str = None) -> dict:
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
        if self._local:
            raise EntityError("Use .export() for local execution.")

        obj = self.to_dict()

        if uuid is None:
            api = api_ctx_create(self.project, DTO_DTIT)
            return self._context.create_object(obj, api)

        self.id = uuid
        api = api_ctx_update(self.project, DTO_DTIT, self.name, uuid)
        return self._context.update_object(obj, api)

    def export(self, filename: str = None) -> None:
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
            else f"dataitem_{self.project}_{self.name}.yaml"
        )
        self._export_object(filename, obj)

    #############################
    #  Dataitem Methods
    #############################

    def as_df(self, file_format: str = None, **kwargs) -> pd.DataFrame:
        """
        Read dataitem as a pandas DataFrame. If the dataitem is not local,
        it will be downloaded to a temporary folder and deleted after the
        method is executed.
        The path of the dataitem is specified in the spec attribute, and
        must be a store aware path, so for example,
        if the dataitem is store on an s3 bucket, the path must be
        s3://<bucket>/<path_to_dataitem>.

        Parameters
        ----------
        file_format : str
            Format of the file, e.g. csv, parquet
        **kwargs
            Keyword arguments.

        Returns
        -------
        pd.DataFrame
            Pandas DataFrame.
        """

        # Get store
        store = get_default_store()
        tmp_path = False

        # Download dataitem if not local
        if self._check_local():
            path = self.spec.path
        else:
            # Check file format then download
            path_ext = get_extension(self.spec.path)
            if path_ext not in ["csv", "parquet"] and file_format is None:
                raise EntityError(
                    "Unknown file format, please specify file_format, e.g. file_format='csv'"
                )
            path = store.download(self.spec.path)
            tmp_path = True

        # Read DataFrame
        extension = file_format if file_format is not None else get_extension(path)
        df = store.read_df(path, extension, **kwargs)

        # Clean temp folder
        if tmp_path:
            if check_file(path):
                path = get_dir(path)
            clean_all(path)

        return df

    def write_df(self, df: pd.DataFrame, target_path: str = None, **kwargs) -> str:
        """
        Write pandas DataFrame as parquet.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to write.
        target_path : str
            Path to write the dataframe to
        **kwargs
            Keyword arguments.

        Returns
        -------
        str
            Path to the written dataframe.
        """

        # Get store
        store = get_default_store()

        # Get target path
        if target_path is None:
            target_path = f"{store.get_root_uri()}/{self.name}.parquet"

        # Write DataFrame
        store.write_df(df, target_path, **kwargs)
        return target_path

    #############################
    #  Helper Methods
    #############################

    def _check_local(self) -> bool:
        """
        Check if source path is local.

        Returns
        -------
        bool
            True if local, False otherwise.
        """
        return get_uri_scheme(self.spec.path) in ["", "file"]

    #############################
    #  Getters and Setters
    #############################

    @property
    def local(self) -> bool:
        """
        Get local flag.
        """
        return self._local

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


def dataitem_from_parameters(
    project: str,
    name: str,
    description: str = "",
    kind: str = "dataitem",
    key: str = None,
    path: str = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str = None,
) -> Dataitem:
    """
    Create dataitem.

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
        Representation of artfact like store://etc..
    path : str
        Path to the dataitem on local file system or remote storage.
    local : bool
        Flag to determine if object has local execution.
    embedded : bool
        Flag to determine if object must be embedded in project.
    uuid : str
        UUID.

    Returns
    -------
    Dataitem
        Dataitem object.
    """
    meta = build_metadata(name=name, description=description)
    spec = build_spec(kind, key=key, path=path)
    return Dataitem(
        project=project,
        name=name,
        kind=kind,
        metadata=meta,
        spec=spec,
        local=local,
        embedded=embedded,
        uuid=uuid,
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
