"""
Spec factory module.
"""
from __future__ import annotations

import typing

from pydantic import BaseModel, ValidationError

from sdk.entities.artifacts.spec.registry import artifact_registry
from sdk.entities.dataitems.spec.registry import dataitem_registry
from sdk.entities.functions.spec.registry import function_registry
from sdk.entities.projects.spec.registry import project_registry
from sdk.entities.runs.spec.registry import run_registry
from sdk.entities.tasks.spec.registry import task_registry
from sdk.entities.workflows.spec.registry import workflow_registry
from sdk.utils.commons import ARTF, DTIT, FUNC, PROJ, RUNS, TASK, WKFL
from sdk.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from sdk.entities.base.spec import Spec, SpecRegistry


class SpecBuilder(dict):
    """
    Spec builder class.
    """

    def register(self, module: str, registry: SpecRegistry) -> None:
        """
        Register a module.

        Parameters
        ----------
        module : str
            The name of the module.
        registry : SpecRegistry
            The registry of Spec objects.
        """
        self[module] = registry

    def build(
        self,
        module: str,
        kind: str,
        ignore_validation: bool = False,
        **kwargs,
    ) -> Spec:
        """
        Build an Spec object with the given parameters.

        Parameters
        ----------
        module : str
            The name of the module.
        kind : str
            The type of Spec to build.
        ignore_validation : bool
            Whether to ignore the validation of the parameters.

        Returns
        -------
        EntitySpec
            An Spec object with the given parameters.
        """
        if not ignore_validation:
            kwargs = self._validate_arguments(module, kind, **kwargs)
        try:
            return self[module][kind]["spec"](**kwargs)
        except KeyError:
            raise EntityError(f"Unsupported spec kind '{kind}' for entity '{module}'")

    def _validate_arguments(self, module: str, kind: str, **kwargs) -> dict:
        """
        Validate the parameters for the given kind of object.

        Parameters
        ----------
        module : str
            The name of the module.
        kind : str
            The kind of the object.
        kwargs : dict
            The parameters to validate.

        Returns
        -------
        dict
            The validated parameters.
        """
        try:
            model: BaseModel = self[module][kind]["model"](**kwargs)
            return model.model_dump()
        except KeyError:
            raise EntityError(f"Unsupported parameters kind: {kind}")
        except ValidationError as err:
            raise EntityError(f"Invalid parameters for kind: {kind}") from err


def build_spec(module: str, kind: str, ignore_validation: bool = False, **kwargs) -> Spec:
    """
    Wrapper for SpecBuilder.build.

    Parameters
    ----------
    kind : str
        The type of Spec to build.
    ignore_validation : bool
        Whether to ignore the validation of the parameters.
    **kwargs
        Keyword arguments.

    Returns
    -------
    EntitySpec
        A Spec object with the given parameters.
    """
    return spec_builder.build(module, kind, ignore_validation, **kwargs)


spec_builder = SpecBuilder()
spec_builder.register(ARTF, artifact_registry)
spec_builder.register(DTIT, dataitem_registry)
spec_builder.register(FUNC, function_registry)
spec_builder.register(PROJ, project_registry)
spec_builder.register(RUNS, run_registry)
spec_builder.register(TASK, task_registry)
spec_builder.register(WKFL, workflow_registry)
