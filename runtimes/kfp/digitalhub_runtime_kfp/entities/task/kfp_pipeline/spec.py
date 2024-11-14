from __future__ import annotations

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction


class TaskSpecKfpPipeline(TaskSpecFunction):
    """
    TaskSpecKfpPipeline specifications.
    """

    def __init__(
        self,
        function: str,
        node_selector: list[dict] | None = None,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list[dict] | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
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


class TaskValidatorKfpPipeline(TaskValidatorFunction):
    """
    TaskValidatorKfpPipeline validator.
    """

    schedule: str = None
    """KFP schedule specifications."""
