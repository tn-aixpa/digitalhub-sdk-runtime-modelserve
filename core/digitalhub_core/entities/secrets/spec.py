"""
Secret base specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.spec import Spec, SpecParams


class SecretSpec(Spec):
    """
    Secret specifications.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """


class SecretParams(SpecParams):
    """
    Secret parameters.
    """


spec_registry = {
    "secret": [SecretSpec, SecretParams],
}
