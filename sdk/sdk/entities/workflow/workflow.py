"""
Workflow module.
"""
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.run.run import Run
from sdk.utils.api import API_CREATE, DTO_WKFL
from sdk.utils.utils import get_uiid
from dataclasses import dataclass


@dataclass
class WorkflowMetadata(EntityMetadata):
    ...


@dataclass
class WorkflowSpec(EntitySpec):
    ...


class Workflow(Entity):
    """
    A class representing a workflow.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str = "workflow",
        metadata: WorkflowMetadata = None,
        spec: WorkflowSpec = None,
        local: bool = False,
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
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.kind = kind
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
        Save workflow into backend.

        Returns
        -------
        dict
            Mapping representaion of Workflow from backend.

        """
        if self._local:
            return self.export()
        api = API_CREATE.format(self.project, DTO_WKFL)
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
        filename = filename if filename is not None else f"workflow_{self.name}.yaml"
        return self.export_object(filename, obj)

    def run(self) -> "Run":
        ...

    def schedule(self) -> "Run":
        ...
