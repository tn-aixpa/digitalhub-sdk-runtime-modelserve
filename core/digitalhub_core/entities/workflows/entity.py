"""
Workflow module.
"""
from __future__ import annotations

import typing
from pathlib import Path

from digitalhub_core.context.builder import get_context
from digitalhub_core.entities._base.entity import Entity
from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities.functions.crud import get_function
from digitalhub_core.utils.api import api_ctx_create, api_ctx_update
from digitalhub_core.utils.generic_utils import build_uuid, get_timestamp
from digitalhub_core.utils.io_utils import write_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.context.context import Context
    from digitalhub_core.entities.workflows.metadata import WorkflowMetadata
    from digitalhub_core.entities.workflows.spec import WorkflowSpec
    from digitalhub_core.entities.workflows.status import WorkflowStatus
    from digitalhub_core.entities.runs.entity import Run
    from digitalhub_core.entities.functions.entity import Function


class Workflow(Entity):
    """
    A class representing a workflow.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: WorkflowMetadata,
        spec: WorkflowSpec,
        status: WorkflowStatus,
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
        metadata : WorkflowMetadata
            Metadata of the object.
        spec : WorkflowSpec
            Specification of the object.
        status : WorkflowStatus
            Status of the object.
        user : str
            Owner of the object.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.id = uuid
        self.kind = kind
        self.key = f"store://{project}/workflows/{kind}/{name}:{uuid}"
        self.metadata = metadata
        self.spec = spec
        self.status = status
        self.user = user

        # Add attributes to be used in the to_dict method
        self._obj_attr.extend(["project", "name", "id", "key"])

    #############################
    #  Save / Export
    #############################

    def save(self, update: bool = False) -> Workflow:
        """
        Save entity into backend.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        Workflow
            Entity saved.
        """
        obj = self.to_dict()

        if not update:
            api = api_ctx_create(self.project, "workflows")
            new_obj = self._context().create_object(api, obj)
            self._update_attributes(new_obj)
            return self

        self.metadata.updated = obj["metadata"]["updated"] = get_timestamp()
        api = api_ctx_update(self.project, "workflows", self.id)
        new_obj = self._context().update_object(api, obj)
        self._update_attributes(new_obj)
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
    #  Workflow Methods
    #############################

    def run(
        self,
        labels: list[dict] | None = None,
        env: list[dict] | None = None,
        secrets: list[str] | None = None,
        schedule: str | None = None,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        values: list | None = None,
        local_execution: bool = False,
        **kwargs,
    ) -> Run:
        """
        Run workflow.

        Parameters
        ----------
        labels : list[dict]
            The labels of the task.
        env : list[dict]
            The env variables of the task. Task parameter.
        secrets : list[str]
            The secrets of the task. Task parameter.
        schedule : str
            The schedule of the task. Task parameter.
        inputs : dict
            Workflow inputs. Run parameter.
        outputs : dict
            Workflow outputs. Run parameter.
        parameters : dict
            Workflow parameters. Run parameter.
        values : list
            Workflow values. Run parameter.
        local_execution : bool
            Flag to determine if object has local execution. Run parameter.
        **kwargs
            Keyword arguments passed to Task builder.

        Returns
        -------
        Run
            Run instance.
        """

        function = get_function(project=self.project, entity_name=self.name)

        # Run function
        run = function.run(
            action="pipeline",
            labels=labels,
            env=env,
            secrets=secrets,
            schedule=schedule,
            inputs=inputs, 
            outputs=outputs, 
            parameters=parameters, 
            values=values, 
            local_execution=local_execution)

        return run

    #############################
    #  Static interface methods
    #############################

    @staticmethod
    def _parse_dict(
        obj: dict,
        validate: bool = True,
    ) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to parse.
        validate : bool
            Flag to determine if validation must be performed.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        project = obj.get("project")
        name = obj.get("name")
        kind = obj.get("kind")
        uuid = build_uuid(obj.get("id"))
        metadata = build_metadata(kind, framework_runtime=kind, **obj.get("metadata", {}))
        spec = build_spec(kind, framework_runtime=kind, validate=validate, **obj.get("spec", {}))
        status = build_status(kind, framework_runtime=kind, **obj.get("status", {}))
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


def workflow_from_parameters(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    git_source: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    **kwargs,
) -> Workflow:
    """
    Create a new Workflow instance with the specified parameters.

    Parameters
    ----------
    project : str
        A string representing the project associated with this workflow.
    name : str
        The name of the workflow.
    kind : str
        Kind of the object.
    uuid : str
        ID of the object in form of UUID.
    git_source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    description : str
        A description of the workflow.
    embedded : bool
        Flag to determine if object must be embedded in project.
    **kwargs
        Spec keyword arguments.

    Returns
    -------
    Workflow
        An instance of the created workflow.
    """
    uuid = build_uuid(uuid)
    spec = build_spec(
        kind,
        framework_runtime=kind,
        **kwargs,
    )
    metadata = build_metadata(
        kind,
        framework_runtime=kind,
        project=project,
        name=name,
        version=uuid,
        description=description,
        source=git_source,
        labels=labels,
        embedded=embedded,
    )
    status = build_status(
        kind,
        framework_runtime=kind,
    )
    return Workflow(
        project=project,
        name=name,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def workflow_from_dict(obj: dict) -> Workflow:
    """
    Create Workflow instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Workflow
        Workflow instance.
    """
    return Workflow.from_dict(obj, validate=False)
