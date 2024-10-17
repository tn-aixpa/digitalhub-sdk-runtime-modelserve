from __future__ import annotations

from digitalhub_runtime_kfp.entities.workflow.kfp.entity import WorkflowKfp
from digitalhub_runtime_kfp.entities.workflow.kfp.spec import WorkflowSpecKfp, WorkflowValidatorKfp
from digitalhub_runtime_kfp.entities.workflow.kfp.status import WorkflowStatusKfp

from digitalhub.entities.workflow._base.builder import WorkflowBuilder


class WorkflowKfpBuilder(WorkflowBuilder):
    """
    WorkflowKfp builder.
    """

    ENTITY_CLASS = WorkflowKfp
    ENTITY_SPEC_CLASS = WorkflowSpecKfp
    ENTITY_SPEC_VALIDATOR = WorkflowValidatorKfp
    ENTITY_STATUS_CLASS = WorkflowStatusKfp
    ENTITY_KIND = "kfp"
