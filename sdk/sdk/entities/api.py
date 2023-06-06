# -----------------
# Backend endpoints
# -----------------

# -----------------
# POST
# -----------------


def create_api(
    proj: str,
    dto: str,
) -> str:
    # PROJ_NAME + DTO
    API_CREATE = "/api/v1/-/{}/{}"
    api = API_CREATE.format(proj, dto)
    return api


def create_api_proj() -> str:
    # PROJ_NAME/UUID
    API_CREATE_PROJECT = "/api/v1/projects"
    api = API_CREATE_PROJECT
    return api


# -----------------
# GET
# -----------------


def read_api(
    proj: str,
    dto: str,
    name: str,
    uuid: str = None,
) -> str:
    if uuid is not None:
        # PROJ_NAME + DTO + DTO_NAME + UUID
        API_READ_VERSION = "/api/v1/-/{}/{}/{}/{}"
        api = API_READ_VERSION.format(proj, dto, name, uuid)
    else:
        API_READ_LATEST = "/api/v1/-/{}/{}/{}/latest"
        api = API_READ_LATEST.format(proj, dto, name)
    return api


def read_api_all(proj: str, dto: str, name: str = None) -> str:
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
    if dto is None:
        # PROJ_NAME/UUID
        API_READ_PROJECT = "/api/v1/projects/{}"
        api = API_READ_PROJECT.format(proj)
    else:
        # PROJ_NAME/UUID + DTO
        API_READ_PROJECT_OBJECTS = "/api/v1/projects/{}/{}"
        api = API_READ_PROJECT_OBJECTS.format(proj, dto)
    return api


# -----------------
# PUT
# -----------------


def update_api(
    proj: str,
    dto: str,
    name: str,
    uuid: str,
) -> str:
    # PROJ_NAME + DTO + DTO_NAME + UUID
    API_UPDATE_VERSION = "/api/v1/-/{}/{}/{}/{}"
    api = API_UPDATE_VERSION.format(proj, dto, name, uuid)
    return api


def update_api_project(proj: str) -> str:
    # PROJ_NAME/UUID
    API_UPDATE_PROJECT = "/api/v1/projects/{}"
    api = API_UPDATE_PROJECT.format(proj)
    return api


# DELETE
def delete_api(
    proj: str,
    dto: str,
    name: str,
    uuid: str = None,
) -> str:
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
    # PROJ_NAME/UUID
    API_DELETE_PROJECT = "/api/v1/projects/{}"
    api = API_DELETE_PROJECT.format(proj)
    return api


# -----------------
# DTOs
# -----------------

DTO_PROJ = "projects"
DTO_ARTF = "artifacts"
DTO_FUNC = "functions"
DTO_WKFL = "workflows"
DTO_DTIT = "dataitems"
