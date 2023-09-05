"""
Models for task specifications.
"""
from pydantic import BaseModel


class ConfigMap(BaseModel):
    """
    ConfigMap model.
    """

    name: str
    """ConfigMap name."""


class Secret(BaseModel):
    """
    Secret model.
    """

    secretName: str
    """Secret name."""


class PersistentVolumeClaim(BaseModel):
    """
    PersistentVolumeClaim model.
    """

    claimName: str
    """PersistentVolumeClaim name."""


class Volume(BaseModel):
    """
    Volume model.
    """

    name: str
    """Volume name."""

    configMap: ConfigMap | None = None
    """ConfigMap model."""

    secret: Secret | None = None
    """Secret model."""

    persistentVolumeClaim: PersistentVolumeClaim | None = None
    """PersistentVolumeClaim model."""


class VolumeMount(BaseModel):
    """
    VolumeMount model.
    """

    name: str
    """Volume mount name."""

    mountPath: str
    """Volume mount path."""


class Env(BaseModel):
    """
    Env variable model.
    """

    name: str
    """Env variable name."""

    value: str
    """Env variable value."""


class Resource(BaseModel):
    """
    Resource model.
    """

    limits: dict
    """Resource limits."""

    requests: dict
    """Resource requests."""


class TaskTaskParams(BaseModel):
    """
    "TaskTaskParams" model.
    """

    volumes: list[Volume] = []
    """Volumes."""

    volume_mounts: list[VolumeMount] = []
    """Volume mounts."""

    env: list[Env] = []
    """Env variables."""

    resources: Resource | None = None
    """Resources restrictions."""
