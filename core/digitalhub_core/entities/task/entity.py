from __future__ import annotations

import typing

from digitalhub_core.entities._base.entity.unversioned import UnversionedEntity
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.entities.run.crud import delete_run, get_run, new_run, run_from_parameters

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities.run.entity import Run
    from digitalhub_core.entities.task.spec import TaskSpec
    from digitalhub_core.entities.task.status import TaskStatus


class Task(UnversionedEntity):
    """
    A class representing a task.
    """

    ENTITY_TYPE = EntityTypes.TASK.value

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: TaskSpec,
        status: TaskStatus,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)
        self.spec: TaskSpec
        self.status: TaskStatus

    ##############################
    #  Task methods
    ##############################

    def run(
        self,
        run_kind: str,
        local_execution: bool = False,
        **kwargs,
    ) -> Run:
        """
        Run task.

        Parameters
        ----------
        run_kind : str
            Kind the object.
        local_execution : bool
            Flag to indicate if the run will be executed locally.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        Run
            Run object.
        """
        return self.new_run(
            project=self.project,
            task=self._get_task_string(),
            kind=run_kind,
            local_execution=local_execution,
            **kwargs,
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
        return f"{self.kind}://{splitted[1]}"

    ##############################
    # CRUD Methods for Run
    ##############################

    def new_run(self, **kwargs) -> Run:
        """
        Create a new run.

        Parameters
        ----------
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        Run
            Run object.
        """
        if kwargs["local_execution"]:
            return run_from_parameters(**kwargs)
        return new_run(**kwargs)

    def get_run(self, entity_key: str) -> Run:
        """
        Get run.

        Parameters
        ----------
        entity_key : str
            Entity key.

        Returns
        -------
        Run
            Run object.
        """
        return get_run(entity_key)

    def delete_run(self, entity_key: str) -> None:
        """
        Delete run.

        Parameters
        ----------
        entity_key : str
            Entity key.

        Returns
        -------
        None
        """
        delete_run(entity_key)
