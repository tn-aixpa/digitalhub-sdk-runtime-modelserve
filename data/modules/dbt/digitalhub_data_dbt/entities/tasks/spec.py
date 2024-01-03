"""
Task Transform specification module.
"""
from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec


class TaskSpecTransform(TaskSpec):
    """Task Transform specification."""

    def __init__(
        self,
        function: str,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, **kwargs)


class TaskParamsTransform(TaskParams):
    """
    TaskParamsTransform model.
    """
