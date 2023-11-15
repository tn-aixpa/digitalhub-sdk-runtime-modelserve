"""
Status factory module.
"""
from __future__ import annotations

import typing

from digitalhub_core.entities._base.status import State
from digitalhub_core.entities.artifacts.status import ArtifactStatus
from digitalhub_core.entities.dataitems.status import DataitemStatus
from digitalhub_core.entities.functions.status import FunctionStatus
from digitalhub_core.entities.projects.status import ProjectStatus
from digitalhub_core.entities.runs.status import RunStatus
from digitalhub_core.entities.tasks.status import TaskStatus
from digitalhub_core.entities.workflows.status import WorkflowStatus
from digitalhub_core.utils.commons import ARTF, DTIT, FUNC, PROJ, RUNS, TASK, WKFL

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.status import Status


class StatusBuilder(dict):
    """
    Status builder class.
    """

    def register(self, module: str, status: Status) -> None:
        """
        Register status.

        Parameters
        ----------
        module: str
            module name.
        status: Status
            Status object.

        Returns
        -------
        None
        """
        self[module] = status

    def build(self, module: str, **kwargs) -> Status:
        """
        Build entity status object.

        Parameters
        ----------
        module: str
            module name.
        **kwargs
            Keyword arguments.

        Returns
        -------
        Status
            An entity status object.
        """
        if module not in self:
            raise ValueError(f"Invalid module name: {module}")
        kwargs = self._parse_arguments(**kwargs)
        return self[module](**kwargs)

    @staticmethod
    def _parse_arguments(**kwargs) -> dict:
        """
        Parse keyword arguments and add default values.

        Parameters
        ----------
        **kwargs
            Keyword arguments.

        Returns
        -------
        dict
            Keyword arguments with default values.
        """
        state = kwargs.get("state")
        if state is None:
            kwargs["state"] = State.CREATED.value
        else:
            if kwargs["state"] not in State.__members__:
                raise ValueError(f"Invalid state: {state}")
        return kwargs


def build_status(module: str, **kwargs) -> Status:
    """
    Wrapper for StatusBuilder.build.

    Parameters
    ----------
    module: str
        module name.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Status
        An entity status object.
    """
    return status_builder.build(module, **kwargs)


status_builder = StatusBuilder()
status_builder.register(ARTF, ArtifactStatus)
status_builder.register(DTIT, DataitemStatus)
status_builder.register(FUNC, FunctionStatus)
status_builder.register(PROJ, ProjectStatus)
status_builder.register(RUNS, RunStatus)
status_builder.register(TASK, TaskStatus)
status_builder.register(WKFL, WorkflowStatus)
