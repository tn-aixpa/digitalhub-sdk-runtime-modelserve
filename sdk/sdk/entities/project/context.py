from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from sdk.entities.project.project import Project


class Context:
    def __init__(self) -> None:
        self._instances = {}
        self._current = None

    def add(self, project: Project) -> None:
        if project.name not in self._instances:
            self._instances[project.name] = project

    def get(self, name: str) -> Project:
        return self._instances.get(name)

    def remove(self, name: str) -> None:
        del self._instances[name]

    def set_current(self, name: str) -> None:
        self._current = name


project_instances = Context()


def set_context(project: Project) -> None:
    project_instances.add(project)
    project_instances.set_current(project.name)


def get_context(project_name: str) -> Project:
    ctx = project_instances.get(project_name)
    if ctx is None:
        raise ValueError(f"Project {project_name} not found in context.")
    return ctx
