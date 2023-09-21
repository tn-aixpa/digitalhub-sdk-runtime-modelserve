"""
Project specification registry module.
"""
from sdk.entities.project.kinds import ProjectKinds
from sdk.entities.project.spec.models import ProjectParams
from sdk.entities.project.spec.objects import ProjectSpecProject

REGISTRY_SPEC = {
    ProjectKinds.PROJECT.value: ProjectSpecProject,
}
REGISTRY_MODEL = {
    ProjectKinds.PROJECT.value: ProjectParams,
}
