"""
Project specification registry module.
"""
from sdk.entities.projects.kinds import ProjectKinds
from sdk.entities.projects.spec.models import ProjectParams
from sdk.entities.projects.spec.objects import ProjectSpecProject

PROJECT_SPEC = {
    ProjectKinds.PROJECT.value: ProjectSpecProject,
}
PROJECT_MODEL = {
    ProjectKinds.PROJECT.value: ProjectParams,
}
