"""
Task spec module.
"""
from sdk.entities.base.spec import EntitySpec


class TaskSpec(EntitySpec):
    """Task specification."""

    def __init__(
        self,
        k8s_resources: dict = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        k8s_resources : dict, optional
            The k8s resources of the task.

        """
        self.k8s_resources = k8s_resources if k8s_resources is not None else {}


def build_spec(kind: str, **kwargs) -> TaskSpec:
    """
    Build a TaskSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of TaskSpec to build.
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    TaskSpec
        A TaskSpec object with the given parameters.

    Raises
    ------
    ValueError
        If the given kind is not supported.
    """
    if kind == "task":
        return TaskSpec(**kwargs)
    raise ValueError(f"Unknown kind: {kind}")
