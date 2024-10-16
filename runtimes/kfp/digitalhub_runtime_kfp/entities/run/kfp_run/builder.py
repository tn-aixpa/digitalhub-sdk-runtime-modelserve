from __future__ import annotations

from digitalhub_runtime_kfp.entities.run.kfp_run.entity import RunKfpRun
from digitalhub_runtime_kfp.entities.run.kfp_run.spec import RunSpecKfpRun, RunValidatorKfpRun
from digitalhub_runtime_kfp.entities.run.kfp_run.status import RunStatusKfpRun

from digitalhub.entities.run._base.builder import RunBuilder


class RunKfpRunBuilder(RunBuilder):
    """
    RunKfpRunBuilder runer.
    """

    ENTITY_CLASS = RunKfpRun
    ENTITY_SPEC_CLASS = RunSpecKfpRun
    ENTITY_SPEC_VALIDATOR = RunValidatorKfpRun
    ENTITY_STATUS_CLASS = RunStatusKfpRun
