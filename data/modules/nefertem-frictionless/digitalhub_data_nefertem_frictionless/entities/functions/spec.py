"""
Nefertem Function specification module.
"""
from __future__ import annotations

from typing import Union

from digitalhub_core.entities.functions.spec import FunctionParams, FunctionSpec
from nefertem_validation_frictionless.constraints import ConstraintFrictionless, ConstraintFullFrictionless


class FunctionSpecNefertemFrictionless(FunctionSpec):
    """
    Specification for a Function Nefertem.
    """

    def __init__(
        self,
        source: str | None = None,
        constraints: list[dict] | None = None,
        error_report: str | None = None,
        metrics: list[dict] | None = None,
        **kwargs,
    ):
        super().__init__(source, **kwargs)
        self.constraints = constraints
        self.error_report = error_report
        self.metrics = metrics


class FunctionParamsNefertemFrictionless(FunctionParams):
    """
    Function Nefertem parameters model.
    """

    constraints: list[Union[ConstraintFrictionless, ConstraintFullFrictionless]] = None
    """List of constraints for the function."""

    error_report: str = None
    """Error report kind for the function."""
