"""
Model base specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.spec import Spec, SpecParams


class ModelSpec(Spec):
    """
    Model specifications.
    """

    def __init__(self, **kwargs) -> None:
        """
        Constructor.
        """

        self._any_setter(**kwargs)


class ModelParams(SpecParams):
    """
    Model parameters.
    """


class ModelSpecModel(ModelSpec):
    """
    Model specifications.
    """

    def __init__(
        self,
        base_model: str | None = None,
        parameters: dict | None = None,
        metrics: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        self.base_model = base_model
        self.parameters = parameters
        self.metrics = metrics

        self._any_setter(**kwargs)


class ModelSpecParams(ModelParams):
    """
    Model parameters.
    """

    base_model: str | None = None

    parameters: dict | None = None

    metrics: dict | None = None
