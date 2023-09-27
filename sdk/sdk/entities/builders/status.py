"""
Status factory module.
"""
from sdk.entities.base.status import Status, StatusState


def build_status(**kwargs) -> Status:
    """
    Build entity status object.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Status
        An entity status object.
    """
    if kwargs:
        if "state" not in kwargs:
            kwargs["state"] = StatusState.CREATED.value
        else:
            if kwargs["state"] not in StatusState.__members__:
                raise ValueError(f"Invalid status status: {kwargs['state']}")
        return Status(**kwargs)
    return Status(state=StatusState.CREATED.value)
