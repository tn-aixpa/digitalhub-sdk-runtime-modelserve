"""
Function module.
"""
from dataclasses import dataclass

from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.run.run import Run

from sdk.entities.api import API_CREATE, DTO_FUNC
from sdk.utils.utils import get_uiid


@dataclass
class FunctionMetadata(EntityMetadata):
    ...


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
        self.metadata = (
            metadata if metadata is not None else FunctionMetadata(name=name)
        )
        self.spec = spec if spec is not None else FunctionSpec()
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
        r = self.save_object(self.to_dict(), api, overwrite)

        return r

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
            else f"function_{self.project}_{self.name}.yaml"
        )
        return self.export_object(filename, obj)

    @classmethod
    def from_dict(cls, d: dict) -> "Function":
        """
        Create Function instance from a dictionary.

        Parameters
        ----------
        d : dict
            Dictionary to create Function from.

        Returns
        -------
        Function
            Function instance.

        """
        project = d.get("project")
        name = d.get("name")
        if project is None or name is None:
            raise Exception("Project or name is not specified.")
        metadata = FunctionMetadata.from_dict(d.get("metadata", {"name": name}))
        spec = FunctionSpec.from_dict(d.get("spec", {}))
        return cls(project, name, metadata=metadata, spec=spec)

    def run(self) -> "Run":
        ...

    def build(self) -> "Run":
        ...

    def deploy(self) -> "Run":
        ...
