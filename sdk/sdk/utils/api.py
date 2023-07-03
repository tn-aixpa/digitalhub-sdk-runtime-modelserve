"""
APIs module.
"""

API_PROJECT = "/api/v1/projects"
API_CONTEXT = "/api/v1/-"

####################
# DTO TYPES
####################

DTO_PROJ = "projects"
DTO_ARTF = "artifacts"
DTO_FUNC = "functions"
DTO_WKFL = "workflows"
DTO_DTIT = "dataitems"

####################
# POST
####################


def create_api(
    proj: str,
    dto: str,
) -> str:
    """
    Create API for a DTO.

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
    # PROJ_NAME + DTO
    return f"{API_CONTEXT}/{proj}/{dto}"


def create_api_proj() -> str:
    """
    Create API for projects.

    Returns
    -------
    str
        The API string formatted.
    """
    # PROJ_NAME/UUID
    return f"{API_PROJECT}"


####################
# GET
####################


def read_api(
    proj: str,
    dto: str,
    name: str,
    uuid: str = None,
) -> str:
    """
    Read API for a DTO.

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
    if uuid is not None:
        # PROJ_NAME + DTO + DTO_NAME + UUID
        return f"{API_CONTEXT}/{proj}/{dto}/{name}/{uuid}"
    # PROJ_NAME + DTO + DTO_NAME + LATEST
    return f"{API_CONTEXT}/{proj}/{dto}/{name}/latest"


def read_api_all(proj: str, dto: str, name: str = None) -> str:
    """
    Read API for a DTO.

    Parameters
    ----------
    proj : str
        The name of the project.
    dto : str
        The type of the DTO.
    name : str, optional
        The name of the DTO. If not provided, all DTOs of the type are returned.

    Returns
    -------
    str
        The API string formatted.
    """
    if name is not None:
        # PROJ_NAME + DTO + DTO_NAME
        return f"{API_CONTEXT}/{proj}/{dto}/{name}"
    # PROJ_NAME + DTO
    return f"{API_CONTEXT}/{proj}/{dto}"


def read_api_project(
    proj: str,
    dto: str = None,
) -> str:
    """
    Read API for projects. If dto is provided, dhcore returns the specific DTO types
    of the project.

    Parameters
    ----------
    proj : str
        The name of the project.
    dto : str, optional
        The type of the DTO. If not provided, the project is returned.

    Returns
    -------
    str
        The API string formatted.
    """
    if dto is None:
        # PROJ_NAME/UUID
        return f"{API_PROJECT}/{proj}"
    # PROJ_NAME/UUID + DTO
    return f"{API_PROJECT}/{proj}/{dto}"


####################
# PUT
####################


def update_api(
    proj: str,
    dto: str,
    name: str,
    uuid: str,
) -> str:
    """
    Update API for a DTO.

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
    # PROJ_NAME + DTO + DTO_NAME + UUID
    return f"{API_CONTEXT}/{proj}/{dto}/{name}/{uuid}"


def update_api_project(proj: str) -> str:
    """
    Update API for projects. Not used.

    Parameters
    ----------
    proj : str
        The name of the project.

    Returns
    -------
    str
        The API string formatted.
    """
    # PROJ_NAME/UUID
    return f"{API_PROJECT}/{proj}"


####################
# DELETE
####################


def delete_api(
    proj: str,
    dto: str,
    name: str,
    uuid: str = None,
) -> str:
    """
    Delete API for a DTO.

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
    if uuid is not None:
        # PROJ_NAME + DTO + DTO_NAME + UUID
        return f"{API_CONTEXT}/{proj}/{dto}/{name}/{uuid}"
    # PROJ_NAME + DTO + DTO_NAME
    return f"{API_CONTEXT}/{proj}/{dto}/{name}"


def delete_api_project(proj: str) -> str:
    """
    Delete API for projects.

    Parameters
    ----------
    proj : str
        The name of the project.

    Returns
    -------
    str
        The API string formatted.
    """
    # PROJ_NAME/UUID
    return f"{API_PROJECT}/{proj}"
