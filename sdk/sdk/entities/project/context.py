from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from sdk.entities.project.project import Project


class Context:
    """
    The context for a project.
    """

    def __init__(self, project: Project) -> None:
        """
        Initialize the context.

        Parameters
        ----------

        project : Project
            The project to create the context for.

        Returns
        -------
        None
        """
        self.name = project.name
        self.client = project.client
        self.local = project.local


class ContextRegistry:
    """
    A registry of contexts.
    """

    def __init__(self) -> None:
        """
        Initialize the registry.
        """
        self._instances = {}

    def add(self, project: Project) -> None:
        """
        Add a context to the registry.

        Parameters
        ----------
        project : Project
            The project to add to the registry.

        Returns
        -------
        None
        """
        if project.name not in self._instances:
            self._instances[project.name] = Context(project)

    def get(self, name: str) -> Context:
        """
        Get the context for the given project name.

        Parameters
        ----------
        name : str
            The name of the project to get the context for.

        Returns
        -------

        Context
            The context for the given project name.
        """
        ctx = self._instances.get(name)
        if ctx is None:
            raise ValueError(f"Context '{name}' not found.")
        return ctx

    def remove(self, name: str) -> None:
        """
        Remove the context for the given project name.

        Parameters
        ----------
        name : str
            The name of the project to remove the context for.

        Returns
        -------
        None
        """
        self._instances.pop(name, None)


project_instances = ContextRegistry()


def set_context(project: Project) -> None:
    """
    Set the current context to the given project.

    Parameters
    ----------
    project : Project
        The project to set as the current context.

    Returns
    -------
    None

    """
    project_instances.add(project)


def get_context(project_name: str) -> Context:
    """
    Get the specific context.

    Parameters
    ----------
    project_name : str
        The name of the project to get the context for.

    Returns
    -------
    Context
        The context for the given project name.

    """
    return project_instances.get(project_name)


def delete_context(project_name: str) -> None:
    """
    Delete the context for the given project name.

    Parameters
    ----------
    project_name : str
        The name of the project to delete the context for.

    Returns
    -------
    None
    """
    project_instances.remove(project_name)
