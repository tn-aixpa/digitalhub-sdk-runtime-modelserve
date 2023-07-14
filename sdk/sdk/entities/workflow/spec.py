"""
Workflow spec module.
"""
from sdk.entities.base.spec import EntitySpec


class WorkflowSpec(EntitySpec):
    """
    Workflow specifications.
    """

    def __init__(self, test: str | None = None) -> None:
        """
        Constructor.

        Parameters
        ----------
        test : str
            Test to run for the workflow.
        """
        self.test = test


class WorkflowSpecJob(WorkflowSpec):
    """
    Specification for a Workflow job.
    """


def build_spec(kind: str, **kwargs) -> WorkflowSpec:
    """
    Build a WorkflowSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of WorkflowSpec to build.
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    WorkflowSpec
        A WorkflowSpecJob object with the given parameters.

    Raises
    ------
    ValueError
        If the given kind is not supported.
    """
    if kind == "job":
        return WorkflowSpecJob(**kwargs)
    raise ValueError(f"Unknown kind: {kind}")
