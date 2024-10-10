from __future__ import annotations

from uuid import uuid4

from pydantic import UUID4, BaseModel


class UUIDValidator(BaseModel):
    """
    Validate UUID format.
    """

    uuid: UUID4


def build_uuid(uuid: str | None = None) -> str:
    """
    Create a uuid if not given. If given, validate it.

    Parameters
    ----------
    uuid : str
        ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).

    Returns
    -------
    str
        Validated UUID4.
    """
    if uuid is not None:
        UUIDValidator(uuid=uuid)
        return uuid
    return str(uuid4())
