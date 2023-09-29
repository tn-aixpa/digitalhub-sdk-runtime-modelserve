"""
Status class module.
"""
from enum import Enum

from sdk.entities.base.base import ModelObj


class State(Enum):
    """
    State enumeration.
    """

    BUILT = "BUILT"
    COMPLETED = "COMPLETED"
    CREATED = "CREATED"
    ERROR = "ERROR"
    IDLE = "IDLE"
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    STOP = "STOP"


class Status(ModelObj):
    """
    Base Status class.
    """

    def __init__(self, state: str) -> None:
        """
        Constructor.

        Parameters
        ----------
        state : str
            The state of the entity.
        """
        self.state = state

    @classmethod
    def from_dict(cls, obj: dict | None = None) -> "Status":
        """
        Return entity specification object from dictionary.

        Parameters
        ----------
        obj : dict
            A dictionary containing the attributes of the entity specification.

        Returns
        -------
        EntitySpec
            An entity specification object.
        """
        obj = obj if obj is not None else {}
        return cls(**obj)
