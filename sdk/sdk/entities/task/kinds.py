"""
Task kind enum module.
"""
from enum import Enum


class TaskKinds(Enum):
    """
    Task kind enum class.
    """

    JOB = "perform"
    BUILD = "build"
    DEPLOY = "deploy"
