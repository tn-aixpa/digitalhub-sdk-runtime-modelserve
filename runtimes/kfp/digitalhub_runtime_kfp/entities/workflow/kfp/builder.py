from __future__ import annotations

from digitalhub_runtime_kfp.entities._base.runtime_entity.builder import RuntimeEntityBuilderKfp
from digitalhub_runtime_kfp.entities.workflow.kfp.entity import WorkflowKfp
from digitalhub_runtime_kfp.entities.workflow.kfp.spec import WorkflowSpecKfp, WorkflowValidatorKfp
from digitalhub_runtime_kfp.entities.workflow.kfp.status import WorkflowStatusKfp
from digitalhub_runtime_kfp.entities.workflow.kfp.utils import source_check

from digitalhub.entities.workflow._base.builder import WorkflowBuilder


class WorkflowKfpBuilder(WorkflowBuilder, RuntimeEntityBuilderKfp):
    """
    WorkflowKfp builder.
    """

    ENTITY_CLASS = WorkflowKfp
    ENTITY_SPEC_CLASS = WorkflowSpecKfp
    ENTITY_SPEC_VALIDATOR = WorkflowValidatorKfp
    ENTITY_STATUS_CLASS = WorkflowStatusKfp
    ENTITY_KIND = "kfp"

    def build(
        self,
        kind: str,
        project: str,
        name: str,
        uuid: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = False,
        **kwargs,
    ) -> WorkflowKfp:
        kwargs = source_check(**kwargs)
        return super().build(
            kind,
            project,
            name,
            uuid,
            description,
            labels,
            embedded,
            **kwargs,
        )
