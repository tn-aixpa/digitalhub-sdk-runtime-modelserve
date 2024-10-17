from __future__ import annotations

import typing
from abc import ABCMeta

from digitalhub.utils.exceptions import BuilderError

if typing.TYPE_CHECKING:
    from digitalhub.runtimes._base import Runtime
    from digitalhub.runtimes.kind_registry import KindRegistry


class RuntimeBuilder(metaclass=ABCMeta):
    """
    Builder class for building runtimes.
    """

    # Class variables
    RUNTIME_CLASS: Runtime = None
    KIND_REGISTRY: KindRegistry = None

    def __init__(self) -> None:
        if self.RUNTIME_CLASS is None:
            raise BuilderError("RUNTIME_CLASS must be set")
        if self.KIND_REGISTRY is None:
            raise BuilderError("KIND_REGISTRY must be set")

    def build(self, *args, **kwargs) -> Runtime:
        """
        Build runtime object.

        Returns
        -------
        Runtime
            Runtime object.
        """
        return self.RUNTIME_CLASS(self.KIND_REGISTRY, *args, **kwargs)
