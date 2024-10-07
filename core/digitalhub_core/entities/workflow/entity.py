from __future__ import annotations

import typing

from digitalhub_core.entities._base.entity.executable import ExecutableEntity
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.runtimes.builder import get_kind_registry
from digitalhub_core.utils.exceptions import BackendError

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities.run.entity import Run
    from digitalhub_core.entities.workflow.spec import WorkflowSpec
    from digitalhub_core.entities.workflow.status import WorkflowStatus


class Workflow(ExecutableEntity):
    """
    A class representing a workflow.
    """

    ENTITY_TYPE = EntityTypes.WORKFLOW.value

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: WorkflowSpec,
        status: WorkflowStatus,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: WorkflowSpec
        self.status: WorkflowStatus

    ##############################
    #  Workflow Methods
    ##############################

    def run(self, action: str | None = None, **kwargs) -> Run:
        """
        Run workflow.

        Parameters
        ----------
        action : str
            Action to execute.
        **kwargs : dict
            Keyword arguments passed to Run builder.

        Returns
        -------
        Run
            Run instance.
        """
        if action is None:
            action = "pipeline"

        # Get kind registry
        kind_reg = get_kind_registry(self.kind)

        # Get task and run kind
        task_kind = kind_reg.get_task_kind_from_action(action=action)
        run_kind = kind_reg.get_run_kind()

        # Create or update new task
        task = self._get_or_create_task(task_kind)

        # Raise error if execution is not done by DHCore backend
        if self._context().local:
            raise BackendError("Cannot run workflow with local backend.")

        return task.run(run_kind, local_execution=False, **kwargs)
