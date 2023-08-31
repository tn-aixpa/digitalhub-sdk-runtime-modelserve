"""
Run Task specification module.
"""
from sdk.entities.task.models import K8sResources
from sdk.entities.task.spec.base import TaskSpec


class TaskSpecRun(TaskSpec):
    """Task Run specification."""

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
        self.volumes = [i.model_dump() for i in res.volumes] if res is not None else []
        self.volume_mounts = (
            [i.model_dump() for i in res.volume_mounts] if res is not None else []
        )
        self.env = [i.model_dump() for i in res.env] if res is not None else []
        self.resources = res.resources.model_dump() if res.resources is not None else {}
