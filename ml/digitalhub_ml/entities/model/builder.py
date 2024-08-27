from __future__ import annotations

import typing

from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.name import build_name
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities._builders.uuid import build_uuid
from digitalhub_core.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from digitalhub_ml.entities.model.entity._base import Model

# Manage class mapper
cls_mapper = {}

try:
    from digitalhub_ml.entities.model.entity.model import ModelModel

    cls_mapper["model"] = ModelModel
except ImportError:
    ...

try:
    from digitalhub_ml.entities.model.entity.mlflow import ModelMlflow

    cls_mapper["mlflow"] = ModelMlflow
except ImportError:
    ...
try:
    from digitalhub_ml.entities.model.entity.sklearn import ModelSklearn

    cls_mapper["sklearn"] = ModelSklearn
except ImportError:
    ...
try:
    from digitalhub_ml.entities.model.entity.huggingface import ModelHuggingface

    cls_mapper["huggingface"] = ModelHuggingface
except ImportError:
    pass


def _choose_model_type(kind: str) -> type[Model]:
    """
    Choose class based on kind.

    Parameters
    ----------
    kind : str
        Kind the object.

    Returns
    -------
    type[Model]
        Class of the model.
    """
    try:
        return cls_mapper[kind]
    except KeyError:
        raise EntityError(f"Unknown model kind: {kind}")


def model_from_parameters(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    path: str | None = None,
    **kwargs,
) -> Model:
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
    labels : list[str]
        List of labels.
    description : str
        Description of the object (human readable).
    embedded : bool
        Flag to determine if object spec must be embedded in project spec.
    path : str
        Object path on local file system or remote storage. It is also the destination path of upload() method.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Model
        Object instance.
    """
    if path is None:
        raise EntityError("Path must be provided.")
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
    cls = _choose_model_type(kind)
    return cls(
        project=project,
        name=name,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def model_from_dict(obj: dict) -> Model:
    """
    Create a new object from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Model
        Object instance.
    """
    kind = obj.get("kind")
    cls = _choose_model_type(kind)
    return cls.from_dict(obj)
