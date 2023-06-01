"""
Function module.
"""
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.run.run import Run
from sdk.utils.api import API_CREATE, DTO_FUNC
from sdk.utils.utils import get_uiid

from dataclasses import dataclass, field


@dataclass
class FunctionMetadata(EntityMetadata):
    name: str


@dataclass
class FunctionSpec(EntitySpec):
    source: str = None
    image: str = None
    tag: str = None
    handler: str = None


class Function(Entity):
    """
    A class representing a function.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str = None,
        metadata: FunctionMetadata = None,
        spec: FunctionSpec = None,
        local: bool = False,
        **kwargs,
    ) -> None:
        """
        Initialize the Function instance.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the function.
        kind : str, optional
            Kind of the function.
        metadata : FunctionMetadata, optional
            Metadata for the function, default is None.
        spec : FunctionSpec, optional
            Specification for the function, default is None.
        local: bool, optional
            Specify if run locally, default is False.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.kind = kind if kind is not None else "local"
        self.metadata = metadata if metadata is not None else {}
        self.spec = spec if spec is not None else {}
        self._local = local

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set id if None
        if self.id is None:
            self.id = get_uiid()

    def save(self, overwrite: bool = False) -> dict:
        """
        Save function into backend.

        Returns
        -------
        dict
            Mapping representaion of Function from backend.

        """
        if self._local:
            raise Exception("Use .export() for local execution.")
        api = API_CREATE.format(self.project, DTO_FUNC)
        return self.save_object(self.to_dict(), api, overwrite)

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
        filename = filename if filename is not None else f"function_{self.name}.yaml"
        return self.export_object(filename, obj)

    def run(self) -> "Run":
        ...

    def build(self) -> "Run":
        ...

    def deploy(self) -> "Run":
        ...
