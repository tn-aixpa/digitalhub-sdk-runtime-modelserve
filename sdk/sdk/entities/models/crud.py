"""
Model operations module.
"""
from __future__ import annotations

import typing

from sdk.context.builder import get_context
from sdk.entities.models.entity import model_from_dict, model_from_parameters
from sdk.utils.api import api_ctx_delete, api_ctx_read, api_ctx_update
from sdk.utils.commons import MDLS
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.models.entity import Model


def create_model(**kwargs) -> Model:
    """
    Create a new Model instance with the specified parameters.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Model
        An instance of the created model.
    """
    return model_from_parameters(**kwargs)


def create_model_from_dict(obj: dict) -> Model:
    """
    Create a new Model instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create the Model from.

    Returns
    -------
    Model
        Model object.
    """
    return model_from_dict(obj)


def new_model(
    project: str,
    name: str,
    description: str | None = None,
    kind: str | None = None,
    embedded: bool = True,
    uuid: str | None = None,
    **kwargs,
) -> Model:
    """
    Create a new Model instance with the specified parameters.

    Parameters
    ----------
    project : str
        A string representing the project associated with this model.
    name : str
        The name of the model.
    description : str
        A description of the model.
    kind : str
        Kind of the object.
    embedded : bool
        Flag to determine if object must be embedded in project.
    uuid : str
        UUID.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Model
        An instance of the created model.
    """
    obj = create_model(
        project=project,
        name=name,
        description=description,
        kind=kind,
        embedded=embedded,
        uuid=uuid,
        **kwargs,
    )
    obj.save()
    return obj


def get_model(project: str, name: str, uuid: str | None = None) -> Model:
    """
    Retrieves model details from the backend.

    Parameters
    ----------

    project : str
        Name of the project.
    name : str
        The name of the model.
    uuid : str
        UUID.

    Returns
    -------
    Model
        Object instance.
    """
    api = api_ctx_read(project, MDLS, name, uuid=uuid)
    obj = get_context(project).read_object(api)
    return model_from_dict(obj)


def import_model(file: str) -> Model:
    """
    Import an Model object from a file using the specified file path.

    Parameters
    ----------
    file : str
        Path to the file.

    Returns
    -------
    Model
        Object instance.
    """
    obj = read_yaml(file)
    return model_from_dict(obj)


def delete_model(project: str, name: str, uuid: str | None = None) -> dict:
    """
    Delete model from the backend. If the uuid is not specified, delete all versions.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the model.
    uuid : str
        UUID.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_delete(project, MDLS, name, uuid=uuid)
    return get_context(project).delete_object(api)


def update_model(model: Model) -> dict:
    """
    Update a model.

    Parameters
    ----------
    model : Model
        The model to update.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_update(model.metadata.project, MDLS, model.metadata.name, uuid=model.id)
    return get_context(model.metadata.project).update_object(model.to_dict(), api)
