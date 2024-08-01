from __future__ import annotations

from enum import Enum


class EntityTypes(Enum):
    """
    Entity types.
    """

    # Must redefine all entity types, no
    # inheritance on enums

    PROJECT = "project"
    ARTIFACT = "artifact"
    SECRET = "secret"
    FUNCTION = "function"
    WORKFLOW = "workflow"
    TASK = "task"
    RUN = "run"
    DATAITEM = "dataitem"
