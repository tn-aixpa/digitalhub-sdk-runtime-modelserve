"""
Dataitem module.
"""
import pandas as pd

from sdk.entities.api import DTO_DTIT, create_api, update_api
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.utils.factories import get_context, get_default_store
from sdk.utils.file_utils import clean_all
from sdk.utils.uri_utils import get_extension
from sdk.utils.utils import get_uiid


class DataitemMetadata(EntityMetadata):
    ...


class DataitemSpec(EntitySpec):
    def __init__(self, key: str = None, path: str = None, **kwargs) -> None:
        """
        Constructor.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments.

        Notes
        -----
        If some of the attributes are not in the signature,
        they will be added as new attributes.
        """
        self.key = key
        self.path = path

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__.keys():
                self.__setattr__(k, v)


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
        self.context = get_context(self.project)

        # Set key in spec store://<project>/dataitems/<kind>/<name>:<uuid>
        self.spec.key = f"store://{self.project}/dataitems/{self.kind}/{self.name}:{self.id}"

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
            raise Exception("Use .export() for local execution.")

        obj = self.to_dict()

        if uuid is None:
            api = create_api(self.project, DTO_DTIT)
            return self.context.client.create_object(obj, api)

        self.id = uuid
        api = update_api(self.project, DTO_DTIT, self.name, uuid)
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
            else f"dataitem_{self.project}_{self.name}.yaml"
        )
        return self.export_object(filename, obj)

    #############################
    #  Dataitem Methods
    #############################

    def as_df(self, format: str = None, **kwargs) -> pd.DataFrame:
        """
        Read dataitem as a pandas DataFrame.

        Parameters
        ----------
        format : str, optional
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

        # Download artifact in temp folder if not local
        if store.is_local():
            path = self.spec.path
        else:
            path = store.download(self.spec.path)

        # Read DataFrame
        extension = format if format is not None else get_extension(path)
        df = self._read_df(path, extension, **kwargs)

        # Clean temp folder
        if not store.is_local():
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
        df.to_parquet(target_path, **kwargs)
        return target_path

    #############################
    #  Helper Methods
    #############################

    def _read_df(self, path: str, extension: str, **kwargs) -> pd.DataFrame:
        """
        Read DataFrame from path.

        Parameters
        ----------
        path : str
            Path to read DataFrame from.
        extension : str
            Extension of the file.
        **kwargs
            Additional keyword arguments for pandas read_csv or read_parquet.

        Returns
        -------
        pd.DataFrame
            Pandas DataFrame.

        Raises
        ------
        Exception
            If format is not supported.
        """
        if extension == "csv":
            return pd.read_csv(path, **kwargs)
        elif extension == "parquet":
            return pd.read_parquet(path, **kwargs)
        raise Exception(f"Format {extension} not supported.")

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
    def from_dict(cls, d: dict) -> "Dataitem":
        """
        Create Dataitem instance from a dictionary.

        Parameters
        ----------
        d : dict
            Dictionary to create Dataitem from.

        Returns
        -------
        Dataitem
            Dataitem instance.

        """
        project = d.get("project")
        name = d.get("name")
        uuid = d.get("id")
        if project is None or name is None:
            raise Exception("Project or name are not specified.")
        metadata = DataitemMetadata.from_dict(d.get("metadata", {"name": name}))
        spec = DataitemSpec.from_dict(d.get("spec", {}))
        return cls(project, name, metadata=metadata, spec=spec, uuid=uuid)
