"""
Task module.
"""
from __future__ import annotations

import typing


from sdk.entities.base.entity import Entity
from sdk.entities.run.crud import new_run
from sdk.entities.task.spec.builder import build_spec
from sdk.entities.utils.utils import get_uiid
from sdk.utils.api import DTO_TASK, api_base_create, api_base_update
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context

if typing.TYPE_CHECKING:
    from sdk.entities.run.entity import Run
    from sdk.entities.task.spec.builder import TaskSpec


class Task(Entity):
    """
    A class representing a task.
    """

    def __init__(
        self,
        project: str,
        task: str,
        uuid: str | None = None,
        kind: str | None = None,
        spec: TaskSpec | None = None,
        local: bool = False,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        project : str
            Name of the project.
        task : str
            Task string.
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        spec : TaskSpec
            Specification of the object.
        local : bool
            If True, run locally.
        **kwargs
            Keyword arguments.
        """
        super().__init__()
        self.project = project
        self.task = task
        self.id = get_uiid(uuid=uuid)
        self.kind = kind if kind is not None else "task"
        self.spec = spec if spec is not None else build_spec(self.kind, **{})

        # Set new attributes
        self._any_setter(**kwargs)

        # Private attributes
        self._local = local
        self._obj_attr += ["task"]
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
            api = api_base_create(DTO_TASK)
            return self._context.create_object(obj, api)

        self.id = uuid
        api = api_base_update(DTO_TASK, self.id)
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

    def run(self, inputs: dict, outputs: list, parameters: dict) -> Run:
        """
        Run task.

        Parameters
        ----------
        task_id : str
            The task id.
        inputs : dict
            The inputs of the run.
        outputs : list
            The outputs of the run.
        parameters : dict
            The parameters of the run.

        Returns
        -------
        Run
            Run object.
        """
        if self._local:
            raise EntityError("Use .run_local() for local execution.")

        run = new_run(
            project=self.project,
            task_id=self.id,
            task=self.task,
            kind="run",
            inputs=inputs,
            outputs=outputs,
            parameters=parameters,
            local=self._local,
        )
        return run

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
        task_id = obj.get("task_id")
        if project is None or task_id is None:
            raise EntityError("Project or task_id are not specified.")

        # Optional fields
        kind = obj.get("kind", "run")
        uuid = obj.get("id")

        # Spec
        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(kind=kind, **spec)

        return {
            "project": project,
            "task_id": task_id,
            "kind": kind,
            "uuid": uuid,
            "spec": spec,
        }


def task_from_parameters(
    project: str,
    kind: str = "task",
    task: str = "",
    resources: dict | None = None,
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
    task : str
        The task string.
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
    spec = build_spec(kind, resources=resources)
    return Task(
        project=project,
        kind="task",
        task=task,
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
