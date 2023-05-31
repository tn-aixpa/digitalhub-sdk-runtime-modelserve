import os

DHUB_CORE_ENDPOINT = os.getenv("DHUB_CORE_ENDPOINT", "http://127.0.0.1:8080")
DHUB_CORE_USER = os.getenv("DHUB_CORE_USER", "")
DHUB_CORE_PASSWORD = os.getenv("DHUB_CORE_PASSWORD", "")
DHUB_CORE_TOKEN = os.getenv("DHUB_CORE_TOKEN", "")

# -----------------
# Backend endpoints
# -----------------

# GET
API_READ_LATEST = "/api/v1/-/{}/{}/{}/latest"  # PROJ_NAME + DTO + DTO_NAME + UUID
API_READ_ALL = "/api/v1/-/{}/{}/{}"  # PROJ_NAME + DTO + DTO_NAME
API_READ_DTO_LATEST = "/api/v1/-/{}/{}"  # PROJ_NAME + DTO
API_READ_VERSION = "/api/v1/-/{}/{}/{}/{}"  # PROJ_NAME + DTO + DTO_NAME + UUID

# POST
API_CREATE = "/api/v1/-/{}/{}"  # PROJ_NAME + DTO

# PUT
API_UPDATE_VERSION = "/api/v1/-/{}/{}/{}/{}"  # PROJ_NAME + DTO + DTO_NAME + UUID

# DELETE
API_DELETE_VERSION = "/api/v1/-/{}/{}/{}/{}"  # PROJ_NAME + DTO + DTO_NAME + UUID
API_DELETE_ALL = "/api/v1/-/{}/{}/{}/{}"  # PROJ_NAME + DTO + DTO_NAME + UUID


# DTOs
DTO_PROJ = "projects"
DTO_ARTF = "artifacts"
DTO_FUNC = "functions"
DTO_WKFL = "workflows"
DTO_DTIT = "dataitems"
