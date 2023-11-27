"""
Task DBT specification module.
"""
from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec

###########################
# Inference
###########################


class TaskSpecInfer(TaskSpec):
    """Task Infer specification."""

    def __init__(
        self,
        function: str,
        run_config: dict,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, **kwargs)
        self.run_config = run_config


class TaskParamsInfer(TaskParams):
    """
    TaskParamsInfer model.
    """

    run_config: dict
    """Nefertem run configuration."""


###########################
# Profiling
###########################


class TaskSpecProfile(TaskSpec):
    """Task Profile specification."""

    def __init__(
        self,
        function: str,
        run_config: dict,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, **kwargs)
        self.run_config = run_config


class TaskParamsProfile(TaskParams):
    """
    TaskParamsProfile model.
    """

    run_config: dict
    """Nefertem run configuration."""


###########################
# Validation
###########################


class TaskSpecValidate(TaskSpec):
    """Task Validate specification."""

    def __init__(
        self,
        function: str,
        run_config: dict,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, **kwargs)
        self.run_config = run_config


class TaskParamsValidate(TaskParams):
    """
    TaskParamsValidate model.
    """

    run_config: dict
    """Nefertem run configuration."""


###########################
# Metric
###########################


class TaskSpecMetric(TaskSpec):
    """Task Metric specification."""

    def __init__(
        self,
        function: str,
        run_config: dict,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, **kwargs)
        self.run_config = run_config


class TaskParamsMetric(TaskParams):
    """
    TaskParamsMetric model.
    """

    run_config: dict
    """Nefertem run configuration."""
