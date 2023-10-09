"""
Task kind enum module.
"""
from enum import Enum


class TaskKinds(Enum):
    """
    Task kind enum class.
    """

    # TODO: change name of perform to job and perform to transform
    JOB = "job"
    BUILD = "build"
    DEPLOY = "deploy"
    TRANSFORM = "transform"
