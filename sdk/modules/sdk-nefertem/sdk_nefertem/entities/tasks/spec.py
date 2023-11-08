"""
Task DBT specification module.
"""
from sdk.entities.tasks.spec import TaskParams, TaskSpec


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
