from __future__ import annotations

from digitalhub.entities._base.spec.base import Spec, SpecValidator


class MaterialSpec(Spec):
    """
    Material specification class.
    """

    def __init__(self, path: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.path = path


class MaterialValidator(SpecValidator):
    """
    Material parameters class.
    """

    path: str
    """Target path to file(s)"""
