"""
Task Python specification module.
"""
from sdk.entities.tasks.spec.objects.base import TaskParams, TaskSpec


class TaskSpecPython(TaskSpec):
    """Task Python specification."""

    def __init__(
        self,
        function: str,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, **kwargs)


class TaskParamsPython(TaskParams):
    """
    TaskParamsPython model.
    """
