from __future__ import annotations

import typing
from concurrent.futures import ThreadPoolExecutor

from digitalhub_core.entities._base.entity.executable import ExecutableEntity
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.runtimes.builder import get_kind_registry
from digitalhub_core.utils.exceptions import BackendError

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities.function.spec import FunctionSpec
    from digitalhub_core.entities.function.status import FunctionStatus
    from digitalhub_core.entities.run.entity import Run


class Function(ExecutableEntity):
    """
    A class representing a function.
    """

    ENTITY_TYPE = EntityTypes.FUNCTION.value

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: FunctionSpec,
        status: FunctionStatus,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: FunctionSpec
        self.status: FunctionStatus

    ##############################
    #  Function Methods
    ##############################

    def run(
        self,
        action: str,
        local_execution: bool = False,
        wait: bool = False,
        log_info: bool = True,
        **kwargs,
    ) -> Run:
        """
        Run function. This method creates a new run and executes it.

        Parameters
        ----------
        action : str
            Action to execute.
        local_execution : bool
            Flag to determine if object has local execution.
        wait : bool
            Flag to wait for execution.
        log_info : bool
            Flag to log information while waiting.
        **kwargs : dict
            Keyword arguments passed to Task and Run builders.

        Returns
        -------
        Run
            Run instance.
        """
        # Get kind registry
        kind_reg = get_kind_registry(self.kind)

        # Get task and run kind
        task_kind = kind_reg.get_task_kind_from_action(action=action)
        run_kind = kind_reg.get_run_kind()

        # Create or update new task
        task = self.new_task(task_kind, **kwargs)

        # Run function from task
        run = task.run(run_kind, local_execution, **kwargs)

        # If execution is done by DHCore backend, return the object
        if not local_execution:
            if self._context().local:
                raise BackendError("Cannot run remote function with local backend.")
            if wait:
                return run.wait(log_info=log_info)
            return run

        # If local execution, build and launch run.
        # Detach the run from the main thread
        run.build()
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = executor.submit(run.run)
            r = result.result()
        return r

    def _get_function_string(self) -> str:
        """
        Get function string.

        Returns
        -------
        str
            Function string.
        """
        return self._get_executable_string()
