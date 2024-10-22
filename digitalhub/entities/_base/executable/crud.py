from __future__ import annotations

from digitalhub.context.api import check_context
from digitalhub.entities._base.executable.entity import ExecutableEntity
from digitalhub.factory.api import build_entity_from_dict
from digitalhub.utils.exceptions import EntityAlreadyExistsError
from digitalhub.utils.io_utils import read_yaml


def import_executable_entity(file: str) -> ExecutableEntity:
    """
    Get object from file.

    Parameters
    ----------
    file : str
        Path to YAML file.

    Returns
    -------
    ExecutableEntity
        Object instance.

    Examples
    --------
    >>> obj = import_context_entity("my-entity.yaml")
    """
    dict_obj: dict | list[dict] = read_yaml(file)
    if isinstance(dict_obj, list):
        exec_dict = dict_obj[0]
        tsk_dicts = dict_obj[1:]
    else:
        exec_dict = dict_obj
        tsk_dicts = []

    check_context(exec_dict["project"])

    obj: ExecutableEntity = build_entity_from_dict(exec_dict)

    obj.import_tasks(tsk_dicts)

    try:
        obj.save()
    except EntityAlreadyExistsError:
        pass
    return obj
