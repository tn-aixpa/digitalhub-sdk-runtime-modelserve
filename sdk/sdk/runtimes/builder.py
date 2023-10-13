"""
Runtime factory module.
"""
from __future__ import annotations

import typing

from sdk.entities.functions.kinds import FunctionKinds

if typing.TYPE_CHECKING:
    from sdk.runtimes.objects.base import Runtime


class RuntimeBuilder:
    """
    Runtime builder class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._modules = {}

    def register(self, function_kind: str, runtime: Runtime) -> None:
        """
        Register runtime.

        Parameters
        ----------
        function_kind : str
            The function kind.
        runtime : Runtime
            Runtime instance.
        """
        self._modules[function_kind] = runtime

    def build(self, function_kind: str) -> Runtime:
        """
        Build runtimes.

        Parameters
        ----------
        function_kind : str
            The function kind.

        Returns
        -------
        Runtime
            Runtime instance.
        """
        if function_kind not in self._modules:
            raise ValueError(f"Runtime {function_kind} not found")
        return self._modules[function_kind]()


def build_runtime(function_kind: str) -> Runtime:
    """
    Wrapper for RuntimeBuilder.build.

    Parameters
    ----------
    function_kind : str
        The function kind.

    Returns
    -------
    Runtime
        Runtime instance.
    """
    return runtime_builder.build(function_kind)


runtime_builder = RuntimeBuilder()


# Handle imports
from sdk.runtimes.objects.python import RuntimePython

runtime_builder.register(FunctionKinds.PYTHON.value, RuntimePython)


try:
    from sdk.runtimes.objects.dbt import RuntimeDBT

    runtime_builder.register(FunctionKinds.DBT.value, RuntimeDBT)
except ImportError:
    ...

try:
    from sdk.runtimes.objects.mlrun import RuntimeMLRun

    runtime_builder.register(FunctionKinds.MLRUN.value, RuntimeMLRun)
except ImportError:
    ...

try:
    from sdk.runtimes.objects.nefertem import RuntimeNefertem

    runtime_builder.register(FunctionKinds.NEFERTEM.value, RuntimeNefertem)
except ImportError:
    ...
