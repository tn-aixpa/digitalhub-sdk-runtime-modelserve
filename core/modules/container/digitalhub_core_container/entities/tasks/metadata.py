from __future__ import annotations

from digitalhub_core.entities.tasks.metadata import TaskMetadata


class TaskMetadataJob(TaskMetadata):
    """
    Task Job metadata.
    """


class TaskMetadataDeploy(TaskMetadata):
    """
    Task Deploy metadata.
    """


class TaskMetadataServe(TaskMetadata):
    """
    Task Serve metadata.
    """
