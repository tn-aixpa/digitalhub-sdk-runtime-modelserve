"""
Task Transform specification module.
"""
from sdk.entities.tasks.spec.objects.base import TaskSpec


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
