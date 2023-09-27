"""
Kinds builder module.
"""
from enum import Enum

from sdk.entities.artifact.kinds import ArtifactKinds
from sdk.entities.dataitem.kinds import DataitemKinds
from sdk.entities.function.kinds import FunctionKinds
from sdk.entities.project.kinds import ProjectKinds
from sdk.entities.run.kinds import RunKinds
from sdk.entities.task.kinds import TaskKinds
from sdk.entities.workflow.kinds import WorkflowKinds
from sdk.utils.commons import ARTF, DTIT, FUNC, PROJ, RUNS, TASK, WKFL
from sdk.utils.exceptions import EntityError


class KindBuilder:
    """
    Builder that create and validate kinds.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._modules = {}

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
        self._modules[module] = {
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
        if module not in self._modules:
            raise EntityError(f"Module '{module}' is not registered.")
        if kind is None:
            return self._modules[module]["default"]
        if kind not in self._modules[module]["values"]:
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
