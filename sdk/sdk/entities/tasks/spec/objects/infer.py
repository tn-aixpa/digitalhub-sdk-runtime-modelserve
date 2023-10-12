"""
Task Infer specification module.
"""
from sdk.entities.tasks.spec.objects.base import TaskParams, TaskSpec


class TaskSpecInfer(TaskSpec):
    """Task Infer specification."""

    def __init__(
        self,
        function: str,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, **kwargs)


class TaskParamsInfer(TaskParams):
    """
    TaskParamsInfer model.
    """
