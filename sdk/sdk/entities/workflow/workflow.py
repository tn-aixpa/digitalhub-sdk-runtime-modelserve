"""
Workflow module.
"""
from dataclasses import dataclass

from sdk.entities.api import DTO_WKFL, create_api, update_api
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.project.context import get_context
from sdk.entities.run.run import Run
from sdk.utils.utils import get_uiid


@dataclass
class WorkflowMetadata(EntityMetadata):
    ...


@dataclass
class WorkflowSpec(EntitySpec):
    test: str = ""


class Workflow(Entity):
    """
    A class representing a workflow.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str = None,
        metadata: WorkflowMetadata = None,
        spec: WorkflowSpec = None,
        local: bool = False,
        embed: bool = True,
        **kwargs,
    ) -> None:
        """
        Initialize the Workflow instance.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the workflow.
        kind : str, optional
            Kind of the workflow, default is 'workflow'.
        metadata : WorkflowMetadata, optional
            Metadata for the workflow, default is None.
        spec : WorkflowSpec, optional
            Specification for the workflow, default is None.
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
        self.kind = kind if kind is not None else "local"
        self.metadata = (
            metadata if metadata is not None else WorkflowMetadata(name=name)
        )
        self.spec = spec if spec is not None else WorkflowSpec()
        self._local = local
        self._embed = embed

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set id if None
        if self.id is None:
            self.id = get_uiid()

        # Set context
        self.context = get_context(self.project)

    def save(self, overwrite: bool = False, uuid: str = None) -> dict:
        """
        Save workflow into backend.

        Parameters
        ----------
        overwrite : bool, optional
            Specify if overwrite, default is False.
        uuid : str, optional
            UUID of the workflow to update, default is None.

        Returns
        -------
        dict
            Mapping representation of Workflow from backend.

        """
        if self._local:
            raise Exception("Use .export() for local execution.")

        if self._embed:
            obj = self.to_dict()
        else:
            obj = self.to_dict_not_embed()

        if overwrite:
            api = update_api(self.project, DTO_WKFL, uuid)
            r = self.context.client.update_object(obj, api)
        else:
            api = create_api(self.project, DTO_WKFL)
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
            else f"workflow_{self.project}_{self.name}.yaml"
        )
        return self.export_object(filename, obj)

    @classmethod
    def from_dict(cls, d: dict) -> "Workflow":
        """
        Create Workflow instance from a dictionary.

        Parameters
        ----------
        d : dict
            Dictionary to create Workflow from.

        Returns
        -------
        Workflow
            Workflow instance.

        """
        project = d.get("project")
        name = d.get("name")
        if project is None or name is None:
            raise Exception("Project or name is not specified.")
        metadata = WorkflowMetadata.from_dict(d.get("metadata", {"name": name}))
        spec = WorkflowSpec.from_dict(d.get("spec", {}))
        return cls(project, name, metadata=metadata, spec=spec)

    def run(self) -> "Run":
        ...

    def schedule(self) -> "Run":
        ...
