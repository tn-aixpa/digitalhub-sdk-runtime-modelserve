"""
Spec factory entity.
"""
from __future__ import annotations

import importlib
import typing

from digitalhub_core.entities.artifacts.spec import ArtifactParams, ArtifactSpec
from digitalhub_core.entities.dataitems.spec import DataitemParams, DataitemSpec
from digitalhub_core.entities.projects.spec import ProjectParams, ProjectSpec
from digitalhub_core.entities.runs.spec import RunParams, RunSpec
from digitalhub_core.entities.workflows.spec import WorkflowParams, WorkflowSpec
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.modules_utils import import_registry
from pydantic import ValidationError

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.spec import Spec


REGISTRY = {
    "artifact": [ArtifactSpec, ArtifactParams],
    "dataitem": [DataitemSpec, DataitemParams],
    "project": [ProjectSpec, ProjectParams],
    "run": [RunSpec, RunParams],
    "workflow": [WorkflowSpec, WorkflowParams],
}


def build_spec(
    entity: str, kind: str, ignore_validation: bool = False, module_kind: str | None = None, **kwargs
) -> Spec:
    """
    Build runtimes.

    Parameters
    ----------
    entity : str
        Type of entity.
    kind : str
        The type of Spec to build.
    ignore_validation : bool
        Whether to ignore the validation of the parameters.
    module_kind : str, optional
        The module to import (for function and tasks).
    **kwargs
        Keyword arguments.


    Returns
    -------
    Spec
        A Spec object with the given parameters.
    """
    try:
        if module_kind is not None:
            # Import registry
            registry = import_registry(module_kind)

            # Get name of module and class
            obj = registry.get_spec(entity, kind)

            # Import spec and model
            module = importlib.import_module(obj.module)
            class_spec = getattr(module, obj.class_spec)
            class_params = getattr(module, obj.class_params)
        else:
            # Get spec and model
            class_spec, class_params = REGISTRY[kind]

        # Validate arguments
        if not ignore_validation:
            kwargs = class_params(**kwargs).dict()

        return class_spec(**kwargs)
    except (ModuleNotFoundError, ImportError):
        raise ValueError(f"Runtime '{kind}' not found")
    except KeyError:
        raise EntityError(f"Unsupported parameters kind '{kind}' for entity {entity}")
    except ValidationError as err:
        raise EntityError(f"Invalid parameters for kind '{kind}' for entity {entity}") from err
