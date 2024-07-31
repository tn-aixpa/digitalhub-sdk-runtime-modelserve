from __future__ import annotations

from enum import Enum


class EntityTypes(Enum):
    """
    Entity types.
    """

    # Must redefine all entity types, no
    # inheritance on enums

    PROJECTS = "project"
    ARTIFACTS = "artifact"
    SECRETS = "secret"
    FUNCTIONS = "function"
    WORKFLOWS = "workflow"
    TASKS = "task"
    RUNS = "run"
    DATAITEMS = "dataitem"
