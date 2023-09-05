"""
State class module.
"""
from enum import Enum

from sdk.entities.base.base_model import ModelObj


class StateStatus(Enum):
    """
    State status enumeration.
    """

    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    CREATED = "CREATED"
    ERROR = "ERROR"
    FAILED = "FAILED"
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"


class State(ModelObj):
    def __init__(self, status: str, **kwargs) -> None:
        """
        Constructor.
        """
        self.status = status

        self._any_setter(**kwargs)

    @classmethod
    def from_dict(cls, obj: dict | None = None) -> "State":
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


def build_state(**kwargs) -> State:
    """
    Build entity state object.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    State
        An entity state object.
    """
    if kwargs:
        if "status" not in kwargs:
            kwargs["status"] = StateStatus.CREATED.value
        else:
            if kwargs["status"] not in StateStatus.__members__:
                raise ValueError(f"Invalid state status: {kwargs['status']}")
        return State(**kwargs)
    return State(status=StateStatus.CREATED.value)
