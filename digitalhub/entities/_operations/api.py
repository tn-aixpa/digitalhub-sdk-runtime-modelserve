from __future__ import annotations

import typing

from digitalhub.entities._operations.processor import processor

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.context.entity import ContextEntity
    from digitalhub.entities._base.executable.entity import ExecutableEntity
    from digitalhub.entities._base.material.entity import MaterialEntity
    from digitalhub.entities._base.project.entity import ProjectEntity


##############################
# CRUD base entity
##############################


def create_project_entity(*args, **kwargs) -> ProjectEntity:
    """
    Wrapper for processor method.
    """
    return processor.create_project_entity(*args, **kwargs)


def read_project_entity(*args, **kwargs) -> ProjectEntity:
    """
    Wrapper for processor method.
    """
    return processor.read_project_entity(*args, **kwargs)


def list_base_entities(*args, **kwargs) -> list[dict]:
    """
    Wrapper for processor method.
    """
    return processor._list_base_entities(*args, **kwargs)


def list_project_entities(*args, **kwargs) -> list[ProjectEntity]:
    """
    Wrapper for processor method.
    """
    return processor.list_project_entities(*args, **kwargs)


def update_project_entity(*args, **kwargs) -> ProjectEntity:
    """
    Wrapper for processor method.
    """
    return processor.update_project_entity(*args, **kwargs)


def delete_project_entity(*args, **kwargs) -> dict:
    """
    Wrapper for processor method.
    """
    return processor.delete_project_entity(*args, **kwargs)


def share_project_entity(*args, **kwargs) -> dict:
    """
    Wrapper for processor method.
    """
    return processor.share_project_entity(*args, **kwargs)


##############################
# CRUD context entity
##############################


def create_context_entity(*args, **kwargs) -> ContextEntity:
    """
    Wrapper for processor method.
    """
    return processor.create_context_entity(*args, **kwargs)


def read_context_entity(*args, **kwargs) -> ContextEntity:
    """
    Wrapper for processor method.
    """
    return processor.read_context_entity(*args, **kwargs)


def read_material_entity(*args, **kwargs) -> MaterialEntity:
    """
    Wrapper for processor method.
    """
    return processor.read_material_entity(*args, **kwargs)


def import_context_entity(*args, **kwargs) -> ContextEntity:
    """
    Wrapper for processor method.
    """
    return processor.import_context_entity(*args, **kwargs)


def import_executable_entity(*args, **kwargs) -> ExecutableEntity:
    """
    Wrapper for processor method.
    """
    return processor.import_executable_entity(*args, **kwargs)


def load_context_entity(*args, **kwargs) -> ContextEntity:
    """
    Wrapper for processor method.
    """
    return processor.load_context_entity(*args, **kwargs)


def load_executable_entity(*args, **kwargs) -> ExecutableEntity:
    """
    Wrapper for processor method.
    """
    return processor.load_executable_entity(*args, **kwargs)


def read_context_entity_versions(*args, **kwargs) -> list[ContextEntity]:
    """
    Wrapper for processor method.
    """
    return processor.read_context_entity_versions(*args, **kwargs)


def read_material_entity_versions(*args, **kwargs) -> list[MaterialEntity]:
    """
    Wrapper for processor method.
    """
    return processor.read_material_entity_versions(*args, **kwargs)


def list_context_entities(*args, **kwargs) -> list[ContextEntity]:
    """
    Wrapper for processor method.
    """
    return processor.list_context_entities(*args, **kwargs)


def list_material_entities(*args, **kwargs) -> list[MaterialEntity]:
    """
    Wrapper for processor method.
    """
    return processor.list_material_entities(*args, **kwargs)


def update_context_entity(*args, **kwargs) -> ContextEntity:
    """
    Wrapper for processor method.
    """
    return processor.update_context_entity(*args, **kwargs)


def delete_context_entity(*args, **kwargs) -> dict:
    """
    Wrapper for processor method.
    """
    return processor.delete_context_entity(*args, **kwargs)


##############################
# Context entity operations
##############################


def read_secret_data(*args, **kwargs) -> dict:
    """
    Wrapper for processor method.
    """
    return processor.read_secret_data(*args, **kwargs)


def update_secret_data(*args, **kwargs) -> None:
    """
    Wrapper for processor method.
    """
    return processor.update_secret_data(*args, **kwargs)


def read_run_logs(*args, **kwargs) -> dict:
    """
    Wrapper for processor method.
    """
    return processor.read_run_logs(*args, **kwargs)


def stop_run(*args, **kwargs) -> None:
    """
    Wrapper for processor method.
    """
    return processor.stop_run(*args, **kwargs)


def resume_run(*args, **kwargs) -> None:
    """
    Wrapper for processor method.
    """
    return processor.resume_run(*args, **kwargs)


def read_files_info(*args, **kwargs) -> list[dict]:
    """
    Wrapper for processor method.
    """
    return processor.read_files_info(*args, **kwargs)


def update_files_info(*args, **kwargs) -> None:
    """
    Wrapper for processor method.
    """
    return processor.update_files_info(*args, **kwargs)


def search_entity(*args, **kwargs) -> dict:
    """
    Wrapper for processor method.
    """
    return processor.search_entity(*args, **kwargs)
