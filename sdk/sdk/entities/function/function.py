"""
Function module.
"""
from dataclasses import dataclass

from sdk.entities.api import DTO_FUNC, create_api, update_api
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.project.context import get_context
from sdk.entities.run.run import Run
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
        embed: bool = False,
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
        embed: bool, optional
            Specify if embed the function, default is False.
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
        self._embed = embed

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set id if None
        if self.id is None:
            self.id = get_uiid()

        self.context = get_context(self.project)

    def save(self, overwrite: bool = False, uuid: str = None) -> dict:
        """
        Save function into backend.

        Parameters
        ----------
        overwrite : bool, optional
            Specify if overwrite existing function, default is False.
        uuid : str, optional
            Specify uuid for the function update, default is None.

        Returns
        -------
        dict
            Mapping representation of Function from backend.

        """
        if self._local:
            raise Exception("Use .export() for local execution.")

        obj = self.to_dict()

        if overwrite:
            api = update_api(self.project, DTO_FUNC, uuid)
            r = self.context.client.update_object(obj, api)
        else:
            api = create_api(self.project, DTO_FUNC)
            r = self.context.client.create_object(obj, api)
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
