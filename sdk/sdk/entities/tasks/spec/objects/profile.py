"""
Task Profile specification module.
"""
from sdk.entities.tasks.spec.objects.base import TaskParams, TaskSpec


class TaskSpecProfile(TaskSpec):
    """Task Profile specification."""

    def __init__(
        self,
        function: str,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, **kwargs)


class TaskParamsProfile(TaskParams):
    """
    TaskParamsProfile model.
    """
