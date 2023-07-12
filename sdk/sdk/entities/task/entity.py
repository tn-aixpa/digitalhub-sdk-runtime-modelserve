"""
Task module.
"""
from __future__ import annotations

import typing
from typing import Self

from sdk.entities.base.entity import Entity
from sdk.entities.run.crud import new_run
from sdk.entities.task.spec import build_spec
from sdk.utils.api import DTO_TASK, api_base_create, api_base_update
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context
from sdk.entities.utils.utils import get_uiid

if typing.TYPE_CHECKING:
    from sdk.entities.task.spec import TaskSpec
    from sdk.entities.run.entity import Run


class Task(Entity):
    """
    A class representing a task.
    """

    def __init__(
        self,
        project: str,
        task: str,
        kind: str,
        spec: TaskSpec,
        local: bool = False,
        uuid: str = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        project : str
            Name of the project.
        kind : str
            The kind of the task.
        spec : TaskSpec
            The specification of the task.
        task : str
            The task string.
        uuid : str, optional
            The uuid of the task.
        local : bool, optional
            Flag to indicate if the task is local or not.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.kind = kind if kind is not None else "task"
        self.spec = spec
        self.id = uuid if uuid is None else get_uiid()
        self.task = task

        self._local = local
        self._obj_attr += ["task"]

        # Set new attributes
        self._any_setter(**kwargs)

        self._context = get_context(self.project)

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str = None) -> dict:
        """
        Save task into backend.

        Parameters
        ----------
        uuid : str, optional
            UUID of the task.

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
        filename = filename if filename is not None else f"task_{self.id}.yaml"
        self._export_object(filename, obj)

    #############################
    #  Task methods
    #############################

    def run(self, inputs: dict, outputs: dict, parameters: dict) -> Run:
        """
        Run task.

        Parameters
        ----------
        task_id : str
            The task id.
        inputs : dict
            The inputs of the run.
        outputs : dict
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

        return new_run(
            project=self.project,
            task_id=self.id,
            task=self.task,
            kind="run",
            inputs=inputs,
            outputs=outputs,
            parameters=parameters,
            local=self._local,
        )

    #############################
    # Generic Methods
    #############################

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        """
        Create object instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        Self
            Self instance.

        """
        parsed_dict = cls._parse_dict(obj)
        obj_ = cls(**parsed_dict)
        obj_._local = obj_._context.local
        return obj_

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
    task: str = None,
    k8s_resources: dict = None,
    local: bool = False,
    uuid: str = None,
) -> Task:
    """
    Create Task object from parameters.

    Parameters
    ----------
    project : str
        Name of the project.
    kind : str, optional
        The kind of the task.
    task : str, optional
        The task string.
    k8s_resources : dict, optional
        The k8s resources.
    local : bool, optional
        Flag to indicate if the task is local or not.
    uuid : str, optional
        UUID.

    Returns
    -------
    Task
        Task object.
    """
    spec = build_spec(kind, k8s_resources=k8s_resources)
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
