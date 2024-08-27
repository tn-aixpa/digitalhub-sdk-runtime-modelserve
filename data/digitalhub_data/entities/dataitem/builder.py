from __future__ import annotations

import typing

from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.name import build_name
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities._builders.uuid import build_uuid
from digitalhub_core.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from digitalhub_data.entities.dataitem.entity._base import Dataitem

# Manage class mapper
cls_mapper = {}
try:
    from digitalhub_data.entities.dataitem.entity.dataitem import DataitemDataitem

    cls_mapper["dataitem"] = DataitemDataitem
except ImportError:
    ...
try:
    from digitalhub_data.entities.dataitem.entity.table import DataitemTable

    cls_mapper["table"] = DataitemTable
except ImportError:
    ...
try:
    from digitalhub_data.entities.dataitem.entity.iceberg import DataitemIceberg

    cls_mapper["iceberg"] = DataitemIceberg
except ImportError:
    pass


def _choose_dataitem_type(kind: str) -> type[Dataitem]:
    """
    Choose class based on kind.

    Parameters
    ----------
    kind : str
        Kind the object.

    Returns
    -------
    type[Dataitem]
        Class of the dataitem.
    """
    try:
        return cls_mapper[kind]
    except KeyError:
        raise EntityError(f"Unknown dataitem kind: {kind}")


def dataitem_from_parameters(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    path: str | None = None,
    **kwargs,
) -> Dataitem:
    """
    Create a new object.

    Parameters
    ----------
    project : str
        Project name.
    name : str
        Object name.
    kind : str
        Kind the object.
    uuid : str
        ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
    description : str
        Description of the object (human readable).
    labels : list[str]
        List of labels.
    embedded : bool
        Flag to determine if object spec must be embedded in project spec.
    path : str
        Object path on local file system or remote storage. It is also the destination path of upload() method.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Dataitem
        Object instance.
    """
    if path is None:
        raise EntityError("Dataitem path must be provided")
    name = build_name(name)
    uuid = build_uuid(uuid)
    metadata = build_metadata(
        kind,
        project=project,
        name=name,
        version=uuid,
        description=description,
        labels=labels,
        embedded=embedded,
    )
    spec = build_spec(
        kind,
        path=path,
        **kwargs,
    )
    status = build_status(kind)
    cls = _choose_dataitem_type(kind)
    return cls(
        project=project,
        name=name,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def dataitem_from_dict(obj: dict) -> Dataitem:
    """
    Create a new object from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Dataitem
        Object instance.
    """
    kind = obj.get("kind")
    cls = _choose_dataitem_type(kind)
    return cls.from_dict(obj)
