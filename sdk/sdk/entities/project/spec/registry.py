"""
Project specification registry module.
"""
from sdk.entities.project.kinds import ProjectKinds
from sdk.entities.project.spec.models import ProjectParams
from sdk.entities.project.spec.objects import ProjectSpecProject

PROJECT_SPEC = {
    ProjectKinds.PROJECT.value: ProjectSpecProject,
}
PROJECT_MODEL = {
    ProjectKinds.PROJECT.value: ProjectParams,
}
