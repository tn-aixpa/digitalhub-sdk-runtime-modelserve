"""
Status class module.
"""
from enum import Enum

from sdk.entities.base.base_model import ModelObj


class StatusState(Enum):
    """
    State enumeration.
    """

    COMPLETED = "COMPLETED"
    CREATED = "CREATED"
    ERROR = "ERROR"
    IDLE = "IDLE"
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    STOP = "STOP"


class Status(ModelObj):
    def __init__(self, state: str, **kwargs) -> None:
        """
        Constructor.

        Parameters
        ----------
        state : str
            The state of the entity.
        **kwargs
            Keyword arguments.
        """
        self.state = state

        self._any_setter(**kwargs)

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
