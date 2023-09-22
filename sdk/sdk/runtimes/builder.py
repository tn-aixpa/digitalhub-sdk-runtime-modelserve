"""
Runtime builder module.
"""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from sdk.runtimes.objects.base import Runtime


class RuntimeBuilder:
    """
    The runtimes builder. It implements the builder pattern to create a Runtime instance.
    """

    def build(
        self, framework: str, action: str, registry: dict, *args, **kwargs
    ) -> Runtime:
        """
        Method to create a runtime instance.

        Parameters
        ----------
        framework : str
            The runtime framework.
        action : str
            The runtime action.
        registry : dict
            The registry of runtimes.
        *args
            Arguments list.
        **kwargs
            Keyword arguments.

        Returns
        -------
        Runtime
            Returns the Runtime instance.
        """
        try:
            return registry[framework](*args, **kwargs)
        except KeyError:
            raise ValueError(
                f"Invalid operation '{action}' for framewrok '{framework}'"
            )
