"""
APIs module.
"""

API_BASE = "/api/v1"
API_CONTEXT = f"{API_BASE}/-"

####################
# DTO TYPES
####################

DTO_PROJ = "projects"
DTO_ARTF = "artifacts"
DTO_FUNC = "functions"
DTO_WKFL = "workflows"
DTO_DTIT = "dataitems"
DTO_TASK = "tasks"
DTO_RUNS = "runs"

####################
# Context APIs
####################


def api_ctx_create(
    proj: str,
    dto: str,
) -> str:
    """
    Create context API.

    Parameters
    ----------
    proj : str
        The name of the project.
    dto : str
        The name of the DTO.

    Returns
    -------
    str
        The API string formatted.
    """
    return f"{API_CONTEXT}/{proj}/{dto}"


def api_ctx_read(
    proj: str,
    dto: str,
    name: str,
    uuid: str = None,
) -> str:
    """
    Read context API.

    Parameters
    ----------
    proj : str
        The name of the project.
    dto : str
        The type of the DTO.
    name : str
        The name of the DTO.
    uuid : str, optional
        The UUID of the DTO. If not provided, the latest version is returned.

    Returns
    -------
    str
        The API string formatted.
    """
    version = f"/{uuid}" if uuid is not None else "/latest"
    return f"{API_CONTEXT}/{proj}/{dto}/{name}{version}"


def api_ctx_update(
    proj: str,
    dto: str,
    name: str,
    uuid: str,
) -> str:
    """
    Update context API.

    Parameters
    ----------
    proj : str
        The name of the project.
    dto : str
        The type of the DTO.
    name : str
        The name of the DTO.
    uuid : str
        The UUID of the DTO.

    Returns
    -------
    str
        The API string formatted.
    """
    return f"{API_CONTEXT}/{proj}/{dto}/{name}/{uuid}"


def api_ctx_delete(
    proj: str,
    dto: str,
    name: str,
    uuid: str = None,
) -> str:
    """
    Delete context API.

    Parameters
    ----------
    proj : str
        The name of the project.
    dto : str
        The type of the DTO.
    name : str
        The name of the DTO.
    uuid : str, optional
        The UUID of the DTO. If not provided, all versions are deleted.

    Returns
    -------
    str
        The API string formatted.
    """
    version = f"/{uuid}" if uuid is not None else ""
    return f"{API_CONTEXT}/{proj}/{dto}/{name}{version}"


####################
# Base controller APIs
####################


def api_base_create(dto: str) -> str:
    """
    Create base API.

    Parameters
    ----------
    dto : str
        The type of the DTO.

    Returns
    -------
    str
        The API string formatted.
    """
    return f"{API_BASE}/{dto}"


def api_base_read(
    dto: str,
    name: str,
) -> str:
    """
    Read base API.

    Parameters
    ----------
    dto : str
        The type of the DTO.
    name : str
        The name of the DTO.

    Returns
    -------
    str
        The API string formatted.
    """
    return f"{API_BASE}/{dto}/{name}"


def api_base_update(dto: str, name: str) -> str:
    """
    Update base API.

    Parameters
    ----------
    dto : str
        The type of the DTO.
    name : str
        The name of the DTO.

    Returns
    -------
    str
        The API string formatted.
    """
    return f"{API_BASE}/{dto}/{name}"


def api_base_delete(dto: str, name: str) -> str:
    """
    Delete base API.

    Parameters
    ----------
    dto : str
        The type of the DTO.
    name : str
        The name of the DTO.

    Returns
    -------
    str
        The API string formatted.
    """
    return f"{API_BASE}/{dto}/{name}"
