"""
Spec factory entity.
"""
from __future__ import annotations

import importlib
import importlib.metadata
import typing

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.spec import Spec


def build_spec(
    entity: str,
    kind: str,
    layer_digitalhub: str | None = None,
    framework_runtime: str | None = None,
    validate: bool = True,
    **kwargs,
) -> Spec:
    """
    Build entity spec object.

    Parameters
    ----------
    entity : str
        Type of entity (e.g. "projects").
    kind : str
        The type of spec to build.
    layer_digitalhub : str
        Layer name (e.g. "digitalhub_core") where the spec is defined.
    framework_runtime : str
        Framework name (e.g. "mlrun", "nefertem") where the spec is defined.
        This referes to the module where the spec is defined. The import
        function will search in different layers.
    validate : bool
        Flag to determine if arguments validation against a pydantic schema must be ignored.

    Returns
    -------
    Spec
        Spec object.
    """
    # Raise error if both layer and framework are not provided or if both are provided.
    # This is because we need some information where to search for the spec class.
    if (layer_digitalhub is None) == (framework_runtime is None):
        raise ValueError("Either layer or framework must be provided, but not both.")

    # If layer is not provided, try to import from runtime, otherwise search by layer.
    if framework_runtime is not None:
        layer_digitalhub = check_module_existence_by_framework(framework_runtime)
    else:
        check_layer_existence(layer_digitalhub)

    # Import registry
    # Note that this requires the creation of a registry whenever a new spec entity is created.
    module_to_import = f"{layer_digitalhub}.entities.{entity}.spec"
    registry = import_registry(module_to_import)

    # Extract class spec and parameters schema from registry by kind
    try:
        class_spec, class_params = registry[kind]
    except KeyError:
        raise ValueError(f"Spec {kind} not found in registry.")
    except ValueError as err:
        raise ValueError(f"Spec registry of module {module_to_import} is not valid: {err}.")

    # Validate arguments
    if validate:
        kwargs = class_params(**kwargs).dict()

    return class_spec(**kwargs)


def check_module_existence_by_framework(framework: str) -> str:
    """
    Try to import registry from implemented module.

    Parameters
    ----------
    framework : str
        Framework name.

    Returns
    -------
    str
        Valid module name.
    """
    # Cycle over digitalhub layers modules (data, ml, ai).
    for layer in ["data", "ml", "ai"]:
        # Try to import module
        module_name = f"digitalhub_{layer}_{framework}"
        try:
            importlib.metadata.distribution(module_name)
            return module_name
        except importlib.metadata.PackageNotFoundError:
            continue
    # If no module is found raise error
    else:
        raise ModuleNotFoundError(f"Module not found in digitalhub layers data, ml, ai for framework {framework}")


def check_layer_existence(layer: str) -> None:
    """
    Check if layer exists.

    Parameters
    ----------
    layer : str
        Layer name.

    Returns
    -------
    None
    """
    try:
        importlib.metadata.distribution(layer)
    except importlib.metadata.PackageNotFoundError:
        raise ModuleNotFoundError(f"Layer {layer} not found.")


def import_registry(module_to_import: str) -> dict[str, list[Spec, Spec]]:
    """
    Import registry from implemented module.

    Parameters
    ----------
    module_to_import : str
        Module name.

    Returns
    -------
    typing.Any
        Registry.
    """
    module = importlib.import_module(module_to_import)
    return getattr(module, "SPEC_REGISTRY")
