from __future__ import annotations

from digitalhub_runtime_kfp.entities.workflow.kfp.models import SourceValidator

from digitalhub.entities.workflow._base.spec import WorkflowSpec, WorkflowValidator


class WorkflowSpecKfp(WorkflowSpec):
    """
    WorkflowSpecKfp specifications.
    """

    def __init__(
        self,
        source: dict | None = None,
        image: str | None = None,
        tag: str | None = None,
        workflow: str | None = None,
    ) -> None:
        super().__init__()

        self.image = image
        self.tag = tag
        self.source = source
        self.workflow = workflow


class WorkflowValidatorKfp(WorkflowValidator):
    """
    WorkflowValidatorKfp validator.
    """

    source: SourceValidator = None
    """Source code validator."""

    image: str = None
    """Name of the Workflow's container image."""

    tag: str = None
    """Tag of the Workflow's container image."""

    workflow: str = None
    """YAML of the Workflow."""