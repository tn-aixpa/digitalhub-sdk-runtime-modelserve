from __future__ import annotations

from digitalhub_core.entities.task.spec import TaskParamsK8s, TaskSpecK8s


class TaskSpecPipeline(TaskSpecK8s):
    """
    Task Pipeline specification.
    """

    def __init__(
        self,
        function: str,
        node_selector: dict | None = None,
        volumes: list | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list | None = None,
        envs: list | None = None,
        secrets: list | None = None,
        profile: str | None = None,
        schedule: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function,
            node_selector,
            volumes,
            resources,
            affinity,
            tolerations,
            envs,
            secrets,
            profile,
            **kwargs,
        )
        self.schedule = schedule


class TaskParamsPipeline(TaskParamsK8s):
    """
    TaskParamsPipeline model.
    """

    schedule: str = None
    """KFP schedule specification."""


class TaskSpecBuild(TaskSpecK8s):
    """
    Task Build specification.
    """


class TaskParamsBuild(TaskParamsK8s):
    """
    TaskParamsBuild model.
    """
