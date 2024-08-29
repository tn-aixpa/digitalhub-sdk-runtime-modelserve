from __future__ import annotations

import typing

from digitalhub_core.context.builder import get_context
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.logger import LOGGER

import digitalhub as dh

if typing.TYPE_CHECKING:
    from digitalhub_ml.entities.project.entity.ml import ProjectMl


def get_model_files(model_key: str, project: str) -> str:
    """
    Get model files.

    Parameters
    ----------
    model_key : str
        The model key.
    project : str
        The project.

    Returns
    -------
    str
        The model files.
    """
    try:
        ctx = get_context(project)
        local = ctx.local
    except ValueError:
        local = False

    try:
        proj: ProjectMl = dh.get_project(project, local=local)
        model = proj.get_model(model_key)
        paths = model.download()
        return paths[0]
    except Exception as e:
        msg = f"Something got wrong during model files collection. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise EntityError(msg) from e
