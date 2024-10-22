from __future__ import annotations

from digitalhub.context.api import check_context
from digitalhub.entities._base.context.entity import ContextEntity
from digitalhub.factory.api import build_entity_from_dict
from digitalhub.utils.exceptions import EntityAlreadyExistsError
from digitalhub.utils.io_utils import read_yaml


def import_context_entity(file: str) -> ContextEntity:
    """
    Get object from file.

    Parameters
    ----------
    file : str
        Path to YAML file.

    Returns
    -------
    ContextEntity
        Object instance.

    Examples
    --------
    >>> obj = import_context_entity("my-entity.yaml")
    """
    dict_obj: dict = read_yaml(file)

    check_context(dict_obj["project"])

    obj = build_entity_from_dict(dict_obj)
    try:
        obj.save()
    except EntityAlreadyExistsError:
        pass
    return obj
