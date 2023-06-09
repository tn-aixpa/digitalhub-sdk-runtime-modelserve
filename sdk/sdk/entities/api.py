"""
APIs module.
"""

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
    API_CREATE = "/api/v1/-/{}/{}"
    api = API_CREATE.format(proj, dto)
    return api


def create_api_proj() -> str:
    """
    Create API for projects.

    Returns
    -------
    str
        The API string formatted.
    """
    # PROJ_NAME/UUID
    API_CREATE_PROJECT = "/api/v1/projects"
    api = API_CREATE_PROJECT
    return api


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
        API_READ_VERSION = "/api/v1/-/{}/{}/{}/{}"
        api = API_READ_VERSION.format(proj, dto, name, uuid)
    else:
        API_READ_LATEST = "/api/v1/-/{}/{}/{}/latest"
        api = API_READ_LATEST.format(proj, dto, name)
    return api


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
        API_READ_ALL = "/api/v1/-/{}/{}/{}"
        api = API_READ_ALL.format(proj, dto, name)
    else:
        # PROJ_NAME + DTO
        API_READ_DTO_LATEST = "/api/v1/-/{}/{}"
        api = API_READ_DTO_LATEST.format(proj, dto, name)
    return api


def read_api_project(
    proj: str,
    dto: str = None,
) -> str:
    """
    Read API for projects.

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
        API_READ_PROJECT = "/api/v1/projects/{}"
        api = API_READ_PROJECT.format(proj)
    else:
        # PROJ_NAME/UUID + DTO
        API_READ_PROJECT_OBJECTS = "/api/v1/projects/{}/{}"
        api = API_READ_PROJECT_OBJECTS.format(proj, dto)
    return api


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
    API_UPDATE_VERSION = "/api/v1/-/{}/{}/{}/{}"
    api = API_UPDATE_VERSION.format(proj, dto, name, uuid)
    return api


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
    API_UPDATE_PROJECT = "/api/v1/projects/{}"
    api = API_UPDATE_PROJECT.format(proj)
    return api


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
        API_DELETE_VERSION = "/api/v1/-/{}/{}/{}/{}"
        api = API_DELETE_VERSION.format(proj, dto, name, uuid)
    else:
        # PROJ_NAME + DTO + DTO_NAME
        API_DELETE_ALL = "/api/v1/-/{}/{}/{}"
        api = API_DELETE_ALL.format(proj, dto, name)
    return api


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
    API_DELETE_PROJECT = "/api/v1/projects/{}"
    api = API_DELETE_PROJECT.format(proj)
    return api


####################
# DTO TYPES
####################

DTO_PROJ = "projects"
DTO_ARTF = "artifacts"
DTO_FUNC = "functions"
DTO_WKFL = "workflows"
DTO_DTIT = "dataitems"
