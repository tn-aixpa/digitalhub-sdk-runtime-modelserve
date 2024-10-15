from __future__ import annotations

from digitalhub.entities._base._base.entity import Base


class Status(Base):
    """
    Base Status class.
    The status class contains information about the state of an entity,
    for example, the state of a RUNNING run, and eventual error message.
    """

    def __init__(self, state: str, message: str | None = None) -> None:
        self.state = state
        self.message = message

    @classmethod
    def from_dict(cls, obj: dict) -> Status:
        """
        Return entity status object from dictionary.

        Parameters
        ----------
        obj : dict
            A dictionary containing the attributes of the entity status.

        Returns
        -------
        EntityStatus
            An entity status object.
        """
        return cls(**obj)
