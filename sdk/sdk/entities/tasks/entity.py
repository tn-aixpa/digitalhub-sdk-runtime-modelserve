"""
Task module.
"""
from __future__ import annotations

import typing

from sdk.context.builder import get_context
from sdk.entities._base.entity import Entity
from sdk.entities._builders.metadata import build_metadata
from sdk.entities._builders.spec import build_spec
from sdk.entities._builders.status import build_status
from sdk.entities.runs.crud import delete_run, get_run, new_run
from sdk.utils.api import api_base_create, api_base_update
from sdk.utils.commons import TASK
from sdk.utils.generic_utils import build_uuid, get_timestamp

if typing.TYPE_CHECKING:
    from sdk.context.context import Context
    from sdk.entities.runs.entity import Run
    from sdk.entities.tasks.metadata import TaskMetadata
    from sdk.entities.tasks.spec import TaskSpec
    from sdk.entities.tasks.status import TaskStatus


class Task(Entity):
    """
    A class representing a task.
    """

    def __init__(
        self,
        uuid: str,
        kind: str,
        metadata: TaskMetadata,
        spec: TaskSpec,
        status: TaskStatus,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        metadata : TaskMetadata
            Metadata of the object.
        spec : TaskSpec
            Specification of the object.
        status : TaskStatus
            Status of the object.
        """
        super().__init__()
        self.id = uuid
        self.kind = kind
        self.metadata = metadata
        self.spec = spec
        self.status = status

        self.project = self.metadata.project
        self._obj_attr.extend(["project"])

    #############################
    #  Save / Export
    #############################

    def save(self, update: bool = False) -> dict:
        """
        Save task into backend.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        dict
            Mapping representation of Task from backend.
        """
        obj = self.to_dict()

        if not update:
            api = api_base_create(TASK)
            return self._context().create_object(obj, api)

        self.metadata.updated = obj["metadata"]["updated"] = get_timestamp()
        api = api_base_update(TASK, self.id)
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
        filename = filename if filename is not None else f"task_{self.id}.yaml"
        self._export_object(filename, obj)

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
    #  Task methods
    #############################

    def run(
        self,
        inputs: dict | None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        local_execution: bool = False,
    ) -> Run:
        """
        Run task.

        Parameters
        ----------
        inputs : dict
            The inputs of the run.
        outputs : dict
            The outputs of the run.
        parameters : dict
            The parameters of the run.
        local_execution : bool
            Flag to indicate if the run will be executed locally.

        Returns
        -------
        Run
            Run object.
        """
        return self.new_run(
            project=self.metadata.project,
            task=self._get_task_string(),
            task_id=self.id,
            kind="run",
            inputs=inputs,
            outputs=outputs,
            parameters=parameters,
            local_execution=local_execution,
        )

    def _get_task_string(self) -> str:
        """
        Get task string.

        Returns
        -------
        str
            Task string.
        """
        splitted = self.spec.function.split("://")
        return f"{splitted[0]}+{self.kind}://{splitted[1]}"

    #############################
    # CRUD Methods for Run
    #############################

    def new_run(self, **kwargs) -> Run:
        """
        Create a new run.

        Parameters
        ----------
        **kwargs
            Keyword arguments.

        Returns
        -------
        Run
            Run object.
        """
        return new_run(**kwargs)

    def get_run(self, uuid: str) -> Run:
        """
        Get run.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        Run
            Run object.
        """
        return get_run(self.metadata.project, uuid)

    def delete_run(self, uuid: str) -> None:
        """
        Delete run.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        None
        """
        delete_run(self.metadata.project, uuid)

    #############################
    #  Overridden Methods
    #############################

    @staticmethod
    def _parse_dict(entity: str, obj: dict) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        entity : str
            Entity type.
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        uuid = build_uuid(obj.get("id"))
        kind = obj.get("kind", "")
        metadata = build_metadata(entity, **obj.get("metadata"))
        spec = build_spec(entity, kind, ignore_validation=True, module_kind=kind, **obj.get("spec"))
        status = build_status(entity, **obj.get("status"))
        return {
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
        }


def task_from_parameters(
    project: str,
    kind: str,
    function: str,
    resources: dict | None = None,
    image: str | None = None,
    base_image: str | None = None,
    uuid: str | None = None,
) -> Task:
    """
    Create Task object from parameters.

    Parameters
    ----------
    project : str
        Name of the project.
    kind : str
        Kind of the object.
    function : str
        The function string.
    resources : dict
        The k8s resources.
    uuid : str
        UUID.

    Returns
    -------
    Task
        Task object.
    """
    uuid = build_uuid(uuid)
    metadata = build_metadata(TASK, project=project, name=uuid)
    spec = build_spec(
        TASK,
        kind,
        module_kind=function.split("://")[0],
        function=function,
        resources=resources,
        image=image,
        base_image=base_image,
    )
    status = build_status(TASK)
    return Task(
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def task_from_dict(obj: dict) -> Task:
    """
    Create Task object from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary representation of Task.

    Returns
    -------
    Task
        Task object.
    """
    return Task.from_dict(TASK, obj)
