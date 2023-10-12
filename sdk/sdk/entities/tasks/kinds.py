"""
Task kind enum module.
"""
from enum import Enum


class TaskKinds(Enum):
    """
    Task kind enum class.
    """

    JOB = "job"
    BUILD = "build"
    DEPLOY = "deploy"
    MLRUN = "mlrun"
    TRANSFORM = "transform"
    VALIDATE = "validate"
    PROFILE = "profile"
    INFER = "infer"
