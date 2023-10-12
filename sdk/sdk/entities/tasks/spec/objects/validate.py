"""
Task Validate specification module.
"""
from sdk.entities.tasks.spec.objects.base import TaskParams, TaskSpec


class TaskSpecValidate(TaskSpec):
    """Task Validate specification."""

    def __init__(
        self,
        function: str,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, **kwargs)


class TaskParamsValidate(TaskParams):
    """
    TaskParamsValidate model.
    """
