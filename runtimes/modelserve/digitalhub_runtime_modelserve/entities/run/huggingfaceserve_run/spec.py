from __future__ import annotations

from digitalhub_runtime_modelserve.entities.run.modelserve_run.spec import (
    RunSpecModelserveRun,
    RunValidatorModelserveRun,
)


class RunSpecHuggingfaceserveRun(RunSpecModelserveRun):
    """RunSpecHuggingfaceserveRun specifications."""


class RunValidatorHuggingfaceserveRun(RunValidatorModelserveRun):
    """RunValidatorHuggingfaceserveRun validator."""
