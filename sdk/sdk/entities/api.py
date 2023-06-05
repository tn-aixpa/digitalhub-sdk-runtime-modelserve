# -----------------
# Backend endpoints
# -----------------

# GET
API_READ_LATEST = "/api/v1/-/{}/{}/{}/latest"  # PROJ_NAME + DTO + DTO_NAME + UUID
API_READ_ALL = "/api/v1/-/{}/{}/{}"  # PROJ_NAME + DTO + DTO_NAME
API_READ_DTO_LATEST = "/api/v1/-/{}/{}"  # PROJ_NAME + DTO
API_READ_VERSION = "/api/v1/-/{}/{}/{}/{}"  # PROJ_NAME + DTO + DTO_NAME + UUID
API_READ_PROJECT = "/api/v1/projects/{}"  # PROJ_NAME/UUID
API_READ_PROJECT_OBJECTS = "/api/v1/projects/{}/{}"  # PROJ_NAME/UUID + DTO

# POST
API_CREATE = "/api/v1/-/{}/{}"  # PROJ_NAME + DTO
API_CREATE_PROJECT = "/api/v1/projects"

# PUT
API_UPDATE_VERSION = "/api/v1/-/{}/{}/{}/{}"  # PROJ_NAME + DTO + DTO_NAME + UUID
API_UPDATE_PROJECT = "/api/v1/projects/{}"  # PROJ_NAME/UUID

# DELETE
API_DELETE_VERSION = "/api/v1/-/{}/{}/{}/{}"  # PROJ_NAME + DTO + DTO_NAME + UUID
API_DELETE_ALL = "/api/v1/-/{}/{}/{}"  # PROJ_NAME + DTO + DTO_NAME
API_DELETE_PROJECT = "/api/v1/projects/{}"  # PROJ_NAME/UUID


# DTOs
DTO_PROJ = "projects"
DTO_ARTF = "artifacts"
DTO_FUNC = "functions"
DTO_WKFL = "workflows"
DTO_DTIT = "dataitems"
