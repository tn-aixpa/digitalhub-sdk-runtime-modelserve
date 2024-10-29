from __future__ import annotations

from pathlib import Path

from digitalhub.entities.utils.entity_types import EntityTypes
from digitalhub.utils.file_utils import eval_zip_sources
from digitalhub.utils.s3_utils import get_s3_bucket


def parse_entity_key(key: str) -> tuple[str]:
    """
    Parse the entity key. Returns project, entity type, kind, name and uuid.

    Parameters
    ----------
    key : str
        The entity key.

    Returns
    -------
    tuple[str]
        Project, entity type, kind, name and uuid.
    """
    try:
        # Remove "store://" from the key
        key = key.replace("store://", "")

        # Split the key into parts
        parts = key.split("/")

        # The project is the first part
        project = parts[0]

        # The entity type is the second part
        entity_type = parts[1]

        # The kind is the third part
        kind = parts[2]

        # Tasks and runs have no name and uuid
        if entity_type in (EntityTypes.TASK.value, EntityTypes.RUN.value):
            name = None
            uuid = parts[3]

        # The name and uuid are separated by a colon in the last part
        else:
            name, uuid = parts[3].split(":")

        return project, entity_type, kind, name, uuid
    except Exception as e:
        raise ValueError("Invalid key format.") from e


def get_entity_type_from_key(key: str) -> str:
    """
    Get entity type.

    Parameters
    ----------
    key : str
        The key of the entity.

    Returns
    -------
    str
        The entity type.
    """
    _, entity_type, _, _, _ = parse_entity_key(key)
    return entity_type


def build_log_path_from_filename(
    project: str,
    entity_type: str,
    name: str,
    uuid: str,
    filename: str,
) -> str:
    """
    Build log path.

    Parameters
    ----------
    project : str
        Project name.
    entity_type : str
        Entity type.
    name : str
        Object name.
    uuid : str
        Object UUID.
    filename : str
        Filename.

    Returns
    -------
    str
        Log path.
    """
    return f"s3://{get_s3_bucket()}/{project}/{entity_type}/{name}/{uuid}/{filename}"


def build_log_path_from_source(
    project: str,
    entity_type: str,
    name: str,
    uuid: str,
    source: str | list[str],
) -> str:
    """
    Build log path.

    Parameters
    ----------
    project : str
        Project name.
    entity_type : str
        Entity type.
    name : str
        Object name.
    uuid : str
        Object UUID.
    source : str | list[str]
        Source(s).

    Returns
    -------
    str
        Log path.
    """
    is_zip = eval_zip_sources(source)
    scheme = "zip+s3" if is_zip else "s3"
    path = f"{scheme}://{get_s3_bucket()}/{project}/{entity_type}/{name}/{uuid}"

    if isinstance(source, list) and len(source) >= 1:
        if len(source) > 1:
            path += "/"
        else:
            path += f"/{Path(source[0]).name}"
    elif Path(source).is_dir():
        path += "/"
    elif Path(source).is_file():
        path += f"/{Path(source).name}"

    return path
