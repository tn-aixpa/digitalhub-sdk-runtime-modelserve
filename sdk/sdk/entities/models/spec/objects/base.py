"""
Model base specification module.
"""
from pydantic import BaseModel

from sdk.entities.base.spec import Spec


class ModelSpec(Spec):
    """
    Model specifications.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """


class ModelParams(BaseModel):
    """
    Model parameters.
    """
