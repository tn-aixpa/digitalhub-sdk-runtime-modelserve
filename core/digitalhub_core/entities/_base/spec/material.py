from __future__ import annotations

from digitalhub_core.entities._base.spec.base import Spec, SpecParams


class MaterialSpec(Spec):
    """
    Material specification class.
    """

    def __init__(self, path: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.path = path


class MaterialParams(SpecParams):
    """
    Material parameters class.
    """

    path: str
    """Target path to file(s)"""
