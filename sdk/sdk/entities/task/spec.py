"""
Task spec module.
"""
from sdk.entities.base.spec import EntitySpec
from sdk.entities.task.models import K8sResources


class TaskSpec(EntitySpec):
    """Task specification."""

    def __init__(
        self,
        resources: dict | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        resources : dict
            The k8s resources of the task.
        """
        resources = resources if resources is not None else {}
        res = K8sResources(**resources) if resources is not None else None
        self.volumes = [i.model_dump() for i in res.volumes]
        self.volume_mounts = [i.model_dump() for i in res.volume_mounts]
        self.env = [i.model_dump() for i in res.env]
        self.resources = res.resources.model_dump() if res.resources is not None else {}


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
