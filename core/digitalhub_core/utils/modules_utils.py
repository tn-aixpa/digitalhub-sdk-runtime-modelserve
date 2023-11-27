"""
Module to organize the import of extension modules.
"""
from __future__ import annotations

import importlib
from collections import namedtuple

from digitalhub_core.utils.commons import FUNC

Rtm = namedtuple("Rtm", ["module", "class_name"])
Obj = namedtuple("Obj", ["module", "class_spec", "class_params"])


class ModuleRegistry:
    """
    Registry for modules to organize the import of classes.

    Attributes
    ----------
    runtime : Rtm
        Runtime class.
    function : Obj
        Function class.
    tasks : dict[str, Obj]
        Tasks classes.

    Methods
    -------
    register_runtime
        Register a runtime class.
    register_function
        Register a function class.
    register_tasks
        Register a task class.
    get_runtime
        Get runtime class.
    get_spec
        Get function or task spec class and validators.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.runtime: Rtm | None = None
        self.function: Obj | None = None
        self.tasks: dict[str, Obj] | None = {}

    def register_runtime(self, module: str, class_name: str) -> None:
        """
        Register a runtime class.

        Parameters
        ----------
        module : str
            Module name.
        class_name : str
            Class name.

        Returns
        -------
        None
        """
        self.runtime = Rtm(module, class_name)

    def register_function(self, module: str, class_spec: str, class_params: str) -> None:
        """
        Register a function class.

        Parameters
        ----------
        module : str
            Module name.
        class_spec : str
            Class spec.
        class_params : str
            Class params.

        Returns
        -------
        None
        """
        self.function = Obj(module, class_spec, class_params)

    def register_tasks(self, kind: str, module: str, class_spec: str, class_params: str) -> None:
        """
        Register a task class.

        Parameters
        ----------
        kind : str
            Task kind.
        module : str
            Module name.
        class_spec : str
            Class spec.
        class_params : str
            Class params.

        Returns
        -------
        None
        """
        self.tasks[kind] = Obj(module, class_spec, class_params)

    def get_runtime(self) -> Obj:
        """
        Get runtime class.

        Returns
        -------
        Obj
            Runtime class.
        """
        return self.runtime

    def get_spec(self, entity: str, kind: str | None = None) -> Obj:
        """
        Get function or task spec class and validators.

        Parameters
        ----------
        entity : str
            Entity type.
        kind : str
            Entity kind.

        Returns
        -------
        Obj
            Spec class.
        """
        if entity == FUNC:
            return self.function
        return self.tasks[kind]


def import_registry(kind: str) -> ModuleRegistry:
    """
    Import registry from implemented module.

    Parameters
    ----------
    kind : str
        Module kind. Basically, the kind of the function due to correspondence
        function-runtime name.

    Returns
    -------
    ModuleRegistry
        Registry.
    """
    try:
        module = importlib.import_module(f"digitalhub_core_{kind}")
        return getattr(module, "registry")
    except (ModuleNotFoundError, ImportError):
        raise ValueError(f"Module digitalhub_core_{kind} not found")
