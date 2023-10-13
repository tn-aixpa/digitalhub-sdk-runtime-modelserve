"""
Spec factory module.
"""
from __future__ import annotations

import typing

from pydantic import BaseModel, ValidationError

from sdk.entities.artifacts.spec.registry import ARTIFACT_MODEL, ARTIFACT_SPEC
from sdk.entities.dataitems.spec.registry import DATAITEM_MODEL, DATAITEM_SPEC
from sdk.entities.functions.spec.registry import FUNCTION_MODEL, FUNCTION_SPEC
from sdk.entities.projects.spec.registry import PROJECT_MODEL, PROJECT_SPEC
from sdk.entities.runs.spec.registry import RUN_MODEL, RUN_SPEC
from sdk.entities.tasks.spec.registry import TASK_MODEL, TASK_SPEC
from sdk.entities.workflows.spec.registry import WORKFLOW_MODEL, WORKFLOW_SPEC
from sdk.utils.commons import ARTF, DTIT, FUNC, PROJ, RUNS, TASK, WKFL
from sdk.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from sdk.entities.base.spec import Spec


class SpecBuilder:
    """
    Builder that create and validate spec.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._modules = {}

    def register(
        self, module: str, registry_spec: dict, registry_models: dict | None = None
    ) -> None:
        """
        Register a module.

        Parameters
        ----------
        module : str
            The name of the module.
        registry_spec : dict
            The registry of Spec objects.
        registry_models : dict
            The registry of Model objects.
        """
        self._modules[module] = {
            "registry_spec": registry_spec,
            "registry_models": registry_models,
        }

    def validate_params(self, module: str, kind: str, **kwargs) -> dict:
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
            model: BaseModel = self._modules[module]["registry_models"][kind](**kwargs)
            return model.model_dump()
        except KeyError:
            raise EntityError(f"Unsupported parameters kind: {kind}")
        except ValidationError as err:
            raise EntityError(f"Invalid parameters for kind: {kind}") from err

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
            kwargs = self.validate_params(module, kind, **kwargs)
        try:
            return self._modules[module]["registry_spec"][kind](**kwargs)
        except KeyError:
            raise EntityError(f"Unsupported spec kind '{kind}' for entity '{module}'")


def build_spec(
    module: str, kind: str, ignore_validation: bool = False, **kwargs
) -> Spec:
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
spec_builder.register(ARTF, ARTIFACT_SPEC, ARTIFACT_MODEL)
spec_builder.register(DTIT, DATAITEM_SPEC, DATAITEM_MODEL)
spec_builder.register(FUNC, FUNCTION_SPEC, FUNCTION_MODEL)
spec_builder.register(PROJ, PROJECT_SPEC, PROJECT_MODEL)
spec_builder.register(RUNS, RUN_SPEC, RUN_MODEL)
spec_builder.register(TASK, TASK_SPEC, TASK_MODEL)
spec_builder.register(WKFL, WORKFLOW_SPEC, WORKFLOW_MODEL)
