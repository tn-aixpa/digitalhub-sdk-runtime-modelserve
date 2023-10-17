"""
Kinds builder module.
"""
from enum import Enum

from sdk.entities.artifacts.kinds import ArtifactKinds
from sdk.entities.dataitems.kinds import DataitemKinds
from sdk.entities.functions.kinds import FunctionKinds
from sdk.entities.projects.kinds import ProjectKinds
from sdk.entities.runs.kinds import RunKinds
from sdk.entities.tasks.kinds import TaskKinds
from sdk.entities.workflows.kinds import WorkflowKinds
from sdk.utils.commons import ARTF, DTIT, FUNC, PROJ, RUNS, TASK, WKFL
from sdk.utils.exceptions import EntityError


class KindBuilder(dict):
    """
    Kind builder class.
    """

    def register(self, module: str, kinds: Enum, default: str) -> None:
        """
        Register a module.

        Parameters
        ----------
        module : str
            Module name.
        kinds : Kind
            Enum class to check.
        default : str
            Default kind.
        """
        self[module] = {
            "default": str(default),
            "values": [str(item.value) for item in kinds],  # type: ignore[attr-defined]
        }

    def build(self, module: str, kind: str | None = None) -> str:
        """
        Build kind for entities.

        Parameters
        ----------
        module : str
            Module name.
        kind : str
            Kind to check. If None, return default kind.

        Returns
        -------
        str
            Entity kind.

        Raises
        ------
        EntityError
            If kind is not valid.
        """
        if module not in self:
            raise EntityError(f"Module '{module}' is not registered.")
        return self._validate_arguments(module, kind)

    def _validate_arguments(self, module: str, kind: str) -> dict:
        """
        Validate kind.

        Parameters
        ----------
        module : str
            Module name.
        kind : str
            Kind to check.
        **kwargs
            Keyword arguments.

        Returns
        -------
        dict
            Keyword arguments with default values.

        Raises
        ------
        EntityError
            If kind is not valid.
        """
        if kind is None:
            return self[module]["default"]
        if kind not in self[module]["values"]:
            raise EntityError(f"Invalid kind '{kind}' for object.")
        return kind


def build_kind(module: str, kind: str | None = None) -> str:
    """
    Wrapper for KindBuilder.build.

    Parameters
    ----------
    module : str
        Module name.
    kind : str
        Kind to check. If None, return default kind.

    Returns
    -------
    str
        Entity kind.

    Raises
    ------
    EntityError
        If kind is not valid.
    """
    return kind_builder.build(module, kind)


kind_builder = KindBuilder()
kind_builder.register(ARTF, ArtifactKinds, ArtifactKinds.ARTIFACT.value)
kind_builder.register(DTIT, DataitemKinds, DataitemKinds.DATAITEM.value)
kind_builder.register(FUNC, FunctionKinds, FunctionKinds.MLRUN.value)
kind_builder.register(PROJ, ProjectKinds, ProjectKinds.PROJECT.value)
kind_builder.register(RUNS, RunKinds, RunKinds.RUN.value)
kind_builder.register(TASK, TaskKinds, TaskKinds.JOB.value)
kind_builder.register(WKFL, WorkflowKinds, WorkflowKinds.WORKFLOW.value)
