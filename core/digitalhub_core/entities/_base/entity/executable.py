from __future__ import annotations

import typing

from digitalhub_core.entities._base.crud import list_entity_api_ctx
from digitalhub_core.entities._base.entity.versioned import VersionedEntity
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.entities.task.crud import delete_task, task_from_dict, task_from_parameters
from digitalhub_core.utils.exceptions import BackendError, EntityError

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities._base.spec.base import Spec
    from digitalhub_core.entities._base.status.base import Status
    from digitalhub_core.entities.task.entity import Task


class ExecutableEntity(VersionedEntity):
    """
    A class representing an entity that can be executed.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: Spec,
        status: Status,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        # Initialize tasks
        self._tasks: dict[str, Task] = {}

    ##############################
    #  Helpers
    ##############################

    def _get_executable_string(self) -> str:
        """
        Get executable string.

        Returns
        -------
        str
            Executable string.
        """
        return f"{self.kind}://{self.project}/{self.name}:{self.id}"

    def import_tasks(self, tasks: list[dict]) -> None:
        """
        Import tasks from yaml.

        Parameters
        ----------
        tasks : list[dict]
            List of tasks to import.

        Returns
        -------
        None
        """
        # Loop over tasks list, in the case where the function
        # is imported from local file.
        for task in tasks:
            # If task is not a dictionary, skip it
            if not isinstance(task, dict):
                continue

            # Create a new object from dictionary.
            # the form in which tasks are stored in function
            # status
            task_obj = task_from_dict(task)

            # Try to save it in backend to been able to use
            # it for launching runs. In fact, tasks must be
            # persisted in backend to be able to launch runs.
            # Ignore if task already exists
            try:
                task_obj.save()
            except BackendError:
                pass

            # Set task if function is the same. Overwrite
            # status task dict with the new task object
            if task_obj.spec.function == self._get_executable_string():
                self._tasks[task_obj.kind] = task_obj

    def new_task(self, task_kind: str, **kwargs) -> Task:
        """
        Create new task.

        Parameters
        ----------
        task_kind : str
            Kind the object.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        Task
            New task.
        """
        # Override kwargs
        kwargs["project"] = self.project
        kwargs["function"] = self._get_executable_string()
        kwargs["kind"] = task_kind

        # Create object instance
        task = task_from_parameters(**kwargs)

        exists, task_id = self._check_task_in_backend(task_kind)

        # Save or update task
        if not exists:
            task.save()
        else:
            task.id = task_id
            task.save(update=True)

        self._tasks[task_kind] = task
        return task

    def update_task(self, kind: str, **kwargs) -> None:
        """
        Update task.

        Parameters
        ----------
        kind : str
            Kind the object.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If task does not exist.
        """
        self._raise_if_not_exists(kind)

        # Update kwargs
        kwargs["project"] = self.project
        kwargs["kind"] = kind
        kwargs["function"] = self._get_executable_string()
        kwargs["uuid"] = self._tasks[kind].id

        # Update task
        task = task_from_parameters(**kwargs)
        task.save(update=True)
        self._tasks[kind] = task

    def get_task(self, kind: str) -> Task:
        """
        Get task.

        Parameters
        ----------
        kind : str
            Kind the object.

        Returns
        -------
        Task
            Task.

        Raises
        ------
        EntityError
            If task is not created.
        """
        self._raise_if_not_exists(kind)
        return self._tasks[kind]

    def delete_task(self, kind: str, cascade: bool = True) -> None:
        """
        Delete task.

        Parameters
        ----------
        kind : str
            Kind the object.
        cascade : bool
            Flag to determine if cascade deletion must be performed.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If task is not created.
        """
        self._raise_if_not_exists(kind)
        delete_task(self._tasks[kind].key, cascade=cascade)
        self._tasks.pop(kind, None)

    def _check_task_in_backend(self, kind: str) -> tuple[bool, str | None]:
        """
        Check if task exists in backend.

        Parameters
        ----------
        kind : str
            Kind the object.

        Returns
        -------
        tuple[bool, str | None]
            Flag to determine if task exists in backend and ID if exists.
        """
        # List tasks from backend filtered by function and kind
        params = {"function": self._get_executable_string(), "kind": kind}
        objs = list_entity_api_ctx(self.project, EntityTypes.TASK.value, params=params)
        try:
            return True, objs[0]["id"]
        except IndexError:
            return False, None

    def _raise_if_not_exists(self, kind: str) -> None:
        """
        Raise error if task is not created.

        Parameters
        ----------
        kind : str
            Kind the object.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If task does not exist.
        """
        if self._tasks.get(kind) is None:
            raise EntityError("Task does not exist.")
