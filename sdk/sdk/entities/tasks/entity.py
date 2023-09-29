"""
Task module.
"""
from __future__ import annotations

import typing

from sdk.context.builder import get_context
from sdk.entities.base.entity import Entity
from sdk.entities.builders.kinds import build_kind
from sdk.entities.builders.spec import build_spec
from sdk.entities.builders.status import build_status
from sdk.entities.runs.crud import delete_run, get_run, new_run
from sdk.utils.api import api_base_create, api_base_update
from sdk.utils.commons import TASK
from sdk.utils.exceptions import EntityError
from sdk.utils.generic_utils import build_uuid

if typing.TYPE_CHECKING:
    from sdk.entities.base.status import Status
    from sdk.entities.runs.entity import Run
    from sdk.entities.tasks.spec.objects.base import TaskSpec


class Task(Entity):
    """
    A class representing a task.
    """

    def __init__(
        self,
        project: str,
        function: str | None = None,
        uuid: str | None = None,
        kind: str | None = None,
        spec: TaskSpec | None = None,
        status: Status | None = None,
        local: bool = False,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        project : str
            Name of the project.
        function : str
            Function string.
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        spec : TaskSpec
            Specification of the object.
        status : Status
            State of the object.
        local : bool
            If True, run locally.
        """
        super().__init__()
        self.project = project
        self.id = build_uuid(uuid=uuid)
        self.function = function if function is not None else ""
        self.kind = kind
        self.spec = spec if spec is not None else build_spec(TASK, self.kind, **{})
        self.status = status if status is not None else build_status(TASK)

        # Private attributes
        self._local = local
        self._obj_attr += ["function"]
        self._context = get_context(self.project)

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str | None = None) -> dict:
        """
        Save task into backend.

        Parameters
        ----------
        uuid : str
            UUID.

        Returns
        -------
        dict
            Mapping representation of Task from backend.
        """
        if self._local:
            raise EntityError("Use .export() for local execution.")

        obj = self.to_dict()

        if uuid is None:
            api = api_base_create(TASK)
            return self._context.create_object(obj, api)

        self.id = uuid
        api = api_base_update(TASK, self.id)
        return self._context.update_object(obj, api)

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
        splitted = self.function.split("://")
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
        kwargs["project"] = self.project
        kwargs["task_id"] = self.id
        kwargs["task"] = self._get_task_string()
        kwargs["local"] = self._local
        return new_run(**kwargs)

    def get_run(self, uuid: str) -> Run:
        """
        Get run.

        Parameters
        ----------
        uuid : str
            UUID.

        Returns
        -------
        Run
            Run object.
        """
        return get_run(self.project, uuid)

    def delete_run(self, uuid: str) -> None:
        """
        Delete run.

        Parameters
        ----------
        uuid : str
            UUID.

        Returns
        -------
        None
        """
        delete_run(self.project, uuid)

    #############################
    # Generic Methods
    #############################

    @classmethod
    def from_dict(cls, obj: dict) -> "Task":
        """
        Create object instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        Task
            Self instance.
        """
        parsed_dict = cls._parse_dict(obj)
        _obj = cls(**parsed_dict)
        _obj._local = _obj._context.local
        return _obj

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
        function = obj.get("function")
        if project is None or function is None:
            raise EntityError("Project or function are not specified.")

        # Optional fields
        kind = obj.get("kind")
        kind = build_kind(TASK, kind)
        uuid = obj.get("id")

        # Build spec, status
        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(TASK, kind=kind, **spec)
        status = obj.get("status")
        status = status if status is not None else {}
        status = build_status(TASK, **status)

        return {
            "project": project,
            "function": function,
            "kind": kind,
            "uuid": uuid,
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
    local: bool = False,
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
    local : bool
        Flag to indicate if the task is local or not.
    uuid : str
        UUID.

    Returns
    -------
    Task
        Task object.
    """
    kind = build_kind(TASK, kind)
    spec = build_spec(
        TASK,
        kind,
        function=function,
        resources=resources,
        image=image,
        base_image=base_image,
    )
    return Task(
        project=project,
        kind=kind,
        function=function,
        spec=spec,
        local=local,
        uuid=uuid,
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
    return Task.from_dict(obj)
