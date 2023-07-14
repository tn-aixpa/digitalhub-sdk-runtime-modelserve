"""
Models for task specifications.
"""
from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


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

    configMap: ConfigMap = None
    """ConfigMap model."""

    secret: Secret = None
    """Secret model."""

    persistentVolumeClaim: PersistentVolumeClaim = None
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


class K8sResources(BaseModel):
    """
    K8sResources model.
    """

    volumes: Optional[list[Volume]] = []
    """Volumes."""

    volume_mounts: Optional[list[VolumeMount]] = []
    """Volume mounts."""

    env: Optional[list[Env]] = []
    """Env variables."""

    resources: Optional[Resource] = None
    """Resources restrictions."""
