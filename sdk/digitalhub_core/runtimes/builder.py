"""
Runtime factory module.
"""
from __future__ import annotations

import importlib
import typing

from digitalhub_core.utils.modules_utils import import_registry

if typing.TYPE_CHECKING:
    from digitalhub_core.runtimes.base import Runtime


def build_runtime(kind: str) -> Runtime:
    """
    Build runtimes.

    Parameters
    ----------
    kind : str
        The runtime kind.

    Returns
    -------
    Runtime
        Runtime instance.
    """
    try:
        registry = import_registry(kind)
        module = importlib.import_module(registry.get_runtime().module)
        return getattr(module, registry.get_runtime().class_name)()
    except (ModuleNotFoundError, ImportError):
        raise ValueError(f"Runtime {kind} not found")
