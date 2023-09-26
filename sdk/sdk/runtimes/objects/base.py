"""
Base Runtime module.
"""
from __future__ import annotations

import typing
from abc import abstractmethod

if typing.TYPE_CHECKING:
    from sdk.entities.run.entity import Run


class Runtime:
    """
    Base Runtime class.
    """

    @abstractmethod
    def run(self) -> Run:
        ...
