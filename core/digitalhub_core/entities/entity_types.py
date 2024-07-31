from __future__ import annotations

from enum import Enum


class EntityTypes(Enum):
    """
    Entity types.
    """

    PROJECTS = "project"
    ARTIFACTS = "artifact"
    SECRETS = "secret"
    FUNCTIONS = "function"
    WORKFLOWS = "workflow"
    TASKS = "task"
    RUNS = "run"
