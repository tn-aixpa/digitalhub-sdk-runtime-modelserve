"""
Task specification models module.
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


class TaskSpec(BaseModel):
    """
    Base task model.
    """

    function: str | None = None
    """Task function."""


class TaskParamsJob(TaskSpec):
    """
    TaskParamsJob model.
    """

    volumes: list[Volume] | None = []
    """Volumes."""

    volume_mounts: list[VolumeMount] | None = []
    """Volume mounts."""

    env: list[Env] | None = []
    """Env variables."""

    resources: Resource | dict | None = {}
    """Resources restrictions."""


class TaskParamsBuild(TaskSpec):
    """
    TaskParamsBuild model.
    """

    image: str
    """Output image name."""

    base_image: str
    """Input image name."""
