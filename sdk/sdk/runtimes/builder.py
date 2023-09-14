"""
Runtime builder module.
"""
from __future__ import annotations

import typing

from sdk.runtimes.registry import REGISTRY_RUNTIMES

if typing.TYPE_CHECKING:
    from sdk.runtimes.objects.base import Runtime


class RuntimeBuilder:
    """
    The runtimes builder. It implements the builder pattern to create a Runtime instance.
    """

    def build(self, kind: str, *args, **kwargs) -> Runtime:
        """
        Method to create a runtime instance.

        Parameters
        ----------
        kind : str
            The runtime kind.
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
            return REGISTRY_RUNTIMES[kind](*args, **kwargs)
        except KeyError:
            raise ValueError(f"Unknown kind: {kind}")
