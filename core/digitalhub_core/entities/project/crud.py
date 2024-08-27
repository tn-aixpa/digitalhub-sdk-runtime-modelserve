from __future__ import annotations

import importlib.util as imputil
import typing
from pathlib import Path

from digitalhub_core.client.builder import build_client, get_client
from digitalhub_core.context.builder import delete_context
from digitalhub_core.entities._base.crud import delete_entity_api_base, read_entity_api_base, update_entity_api_base
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.entities.project.builder import project_from_dict, project_from_parameters
from digitalhub_core.utils.exceptions import BackendError, EntityError
from digitalhub_core.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.project.entity._base import Project


ENTITY_TYPE = EntityTypes.PROJECT.value


def new_project(
    name: str,
    description: str | None = None,
    labels: list[str] | None = None,
    local: bool = False,
    config: dict | None = None,
    context: str | None = None,
    setup_kwargs: dict | None = None,
    **kwargs,
) -> Project:
    """
    Create a new object.

    Parameters
    ----------
    name : str
        Object name.
    description : str
        Description of the object (human readable).
    labels : list[str]
        List of labels.
    local : bool
        If True, use local backend, if False use DHCore backend. Default to False.
    config : dict
        DHCore environment configuration.
    context : str
        The context local folder of the project.
    setup_kwargs : dict
        Setup keyword arguments passed to setup_project() function.
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    Project
        Object instance.

    Examples
    --------
    >>> obj = new_project("my-project")
    """
    build_client(local, config)
    if context is None:
        context = name
    obj = project_from_parameters(
        name=name,
        kind="project",
        description=description,
        labels=labels,
        local=local,
        context=context,
        **kwargs,
    )
    obj.save()
    return _setup_project(obj, setup_kwargs)


def get_project(
    name: str,
    local: bool = False,
    config: dict | None = None,
    setup_kwargs: dict | None = None,
    **kwargs,
) -> Project:
    """
    Retrieves project details from backend.

    Parameters
    ----------
    name : str
        The Project name.
    local : bool
        Flag to determine if backend is local.
    config : dict
        DHCore environment configuration.
    setup_kwargs : dict
        Setup keyword arguments passed to setup_project() function.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    Project
        Object instance.

    Examples
    --------
    >>> obj = get_project("my-project")
    """
    build_client(local, config)
    client = get_client(local)
    obj = read_entity_api_base(client, ENTITY_TYPE, name, **kwargs)
    obj["local"] = local
    project = project_from_dict(obj)
    return _setup_project(project, setup_kwargs)


def import_project(
    file: str,
    local: bool = False,
    config: dict | None = None,
    setup_kwargs: dict | None = None,
) -> Project:
    """
    Import object from a YAML file.

    Parameters
    ----------
    file : str
        Path to YAML file.
    local : bool
        Flag to determine if backend is local.
    config : dict
        DHCore environment configuration.
    setup_kwargs : dict
        Setup keyword arguments passed to setup_project() function.

    Returns
    -------
    Project
        Object instance.

    Examples
    --------
    >>> obj = import_project("my-project.yaml")
    """
    build_client(local, config)
    obj: dict = read_yaml(file)
    obj["local"] = local
    project = project_from_dict(obj)
    return _setup_project(project, setup_kwargs)


def load_project(
    name: str | None = None,
    filename: str | None = None,
    local: bool = False,
    config: dict | None = None,
    setup_kwargs: dict | None = None,
    **kwargs,
) -> Project:
    """
    Load project and context from backend or file. Name or
    filename must be provided. Name takes precedence over filename.

    Parameters
    ----------
    name : str
        Project name.
    filename : str
        Path to YAML file.
    local : bool
        Flag to determine if backend is local.
    config : dict
        DHCore environment configuration.
    setup_kwargs : dict
        Setup keyword arguments passed to setup_project() function.
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    Project
        Object instance.

    Examples
    --------
    If name is provided, load project from backend.
    >>> obj = load_project(name="my-project")

    If filename is provided, load project from file.
    >>> obj = load_project(filename="my-project.yaml")
    """
    if name is not None:
        return get_project(name=name, local=local, config=config, setup_kwargs=setup_kwargs, **kwargs)
    if filename is not None:
        return import_project(filename, local=local, config=config, setup_kwargs=setup_kwargs)
    raise EntityError("Either name or filename must be provided.")


def get_or_create_project(
    name: str,
    local: bool = False,
    config: dict | None = None,
    context: str | None = None,
    setup_kwargs: dict | None = None,
    **kwargs,
) -> Project:
    """
    Try to get project. If not exists, create it.

    Parameters
    ----------
    name : str
        Project name.
    local : bool
        Flag to determine if backend is local.
    config : dict
        DHCore environment configuration.
    context : str
        Folder where the project will saves its context locally.
    setup_kwargs : dict
        Setup keyword arguments passed to setup_project() function.
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    Project
        Object instance.
    """
    try:
        return get_project(
            name,
            local=local,
            config=config,
            setup_kwargs=setup_kwargs,
            **kwargs,
        )
    except BackendError:
        return new_project(
            name,
            local=local,
            config=config,
            setup_kwargs=setup_kwargs,
            context=context,
            **kwargs,
        )


def update_project(entity: Project, local: bool = False, **kwargs) -> Project:
    """
    Update object. Note that object spec are immutable.

    Parameters
    ----------
    entity : Project
        Object to update.
    local : bool
        Flag to determine if backend is local.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    Project
        The updated object.

    Examples
    --------
    >>> obj = update_project(obj)
    """
    client = get_client(local)
    obj = update_entity_api_base(client, ENTITY_TYPE, entity.name, entity.to_dict(), **kwargs)
    return project_from_dict(obj)


def delete_project(
    name: str,
    cascade: bool = True,
    clean_context: bool = True,
    local: bool = False,
    **kwargs,
) -> list[dict]:
    """
    Delete a project.

    Parameters
    ----------
    name : str
        Project name.
    cascade : bool
        Flag to determine if delete is cascading.
    clean_context : bool
        Flag to determine if context will be deleted. If a context is deleted,
        all its objects are unreacheable.
    local : bool
        Flag to determine if backend is local.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    dict
        Response from backend.

    Examples
    --------
    >>> delete_project("my-project")
    """
    client = get_client(local)
    obj = delete_entity_api_base(client, ENTITY_TYPE, name, cascade=cascade, **kwargs)
    if clean_context:
        delete_context(name)
    return obj


def _setup_project(project: Project, setup_kwargs: dict | None = None) -> Project:
    """
    Search for setup_project.py file and launch setup hanlder as project hook.

    Parameters
    ----------
    project : Project
        The project to scafold.
    setup_kwargs : dict
        Arguments to pass to setup handler.

    Returns
    -------
    Project
        Set up project.
    """
    setup_kwargs = setup_kwargs if setup_kwargs is not None else {}
    check_pth = Path(project.spec.context, ".CHECK")
    setup_pth = Path(project.spec.context, "setup_project.py")
    if setup_pth.exists() and not check_pth.exists():
        spec = imputil.spec_from_file_location("setup_project", setup_pth)
        mod = imputil.module_from_spec(spec)
        spec.loader.exec_module(mod)
        handler = getattr(mod, "setup")
        project = handler(project, **setup_kwargs)
        check_pth.touch()
    return project
