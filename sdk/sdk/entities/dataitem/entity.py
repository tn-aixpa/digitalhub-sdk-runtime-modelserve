"""
Dataitem module.
"""
from __future__ import annotations

import typing

from sdk.entities.base.entity import Entity
from sdk.entities.dataitem.metadata import DataitemMetadata
from sdk.entities.dataitem.spec import DataitemSpec
from sdk.utils.api import DTO_DTIT, api_ctx_create, api_ctx_update
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context, get_default_store
from sdk.utils.file_utils import check_file, clean_all, get_dir
from sdk.utils.uri_utils import get_extension, get_uri_scheme
from sdk.utils.utils import get_uiid

if typing.TYPE_CHECKING:
    import pandas as pd


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
        embed: bool = False,
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
        kind : str, optional
            Kind of the dataitem, default is 'dataitem'.
        metadata : DataitemMetadata, optional
            Metadata for the dataitem, default is None.
        spec : DataitemSpec, optional
            Specification for the dataitem, default is None.
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
        self.kind = kind if kind is not None else "dataitem"
        self.metadata = (
            metadata if metadata is not None else DataitemMetadata(name=name)
        )
        self.spec = spec if spec is not None else DataitemSpec()
        self.embedded = embed
        self.id = uuid if uuid is not None else get_uiid()

        self._local = local

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

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
        uuid : str, optional
            Specify uuid for the dataitem to update, default is None.

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
        file_format : str, optional
            Format of the file, e.g. csv, parquet, default is None.
        **kwargs
            Additional keyword arguments for pandas read_csv or read_parquet.

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
        target_path : str, optional
            Path to write the dataframe to, default is None.
        **kwargs
            Additional keyword arguments for pandas.

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
    def from_dict(cls, obj: dict) -> "Dataitem":
        """
        Create Dataitem instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create Dataitem from.

        Returns
        -------
        Dataitem
            Dataitem instance.

        """
        project = obj.get("project")
        name = obj.get("name")
        uuid = obj.get("id")
        if project is None or name is None:
            raise EntityError("Project or name are not specified.")
        metadata = DataitemMetadata.from_dict(obj.get("metadata", {"name": name}))
        spec = DataitemSpec.from_dict(obj.get("spec", {}))
        return cls(project, name, metadata=metadata, spec=spec, uuid=uuid)
