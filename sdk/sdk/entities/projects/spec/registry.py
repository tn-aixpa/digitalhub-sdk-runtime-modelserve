"""
Project specification registry module.
"""
from sdk.entities.base.spec import SpecRegistry
from sdk.entities.projects.kinds import ProjectKinds
from sdk.entities.projects.spec.objects.project import ProjectParamsProject, ProjectSpecProject

project_registry = SpecRegistry()
project_registry.register(ProjectKinds.PROJECT.value, ProjectSpecProject, ProjectParamsProject)
