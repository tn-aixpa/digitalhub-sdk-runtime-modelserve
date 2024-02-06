"""
Models for task specifications.
"""
from __future__ import annotations

from typing import Union
from pydantic import BaseModel
from typing_extensions import Literal


class Volume(BaseModel):
    """
    Volume model.
    """

    volume_type: Literal["config_map", "secret", "persistent_volume_claim"]
    """Volume type."""

    name: str
    """Volume name."""

    spec: Union[VolumeConfigMap, VolumeSecret, VolumePVC]

class VolumeConfigMap(BaseModel):
    """
    Spec for config map volume.
    """
    mount_path: str
    """Volume mount path inside the container."""

    items: list[str] = None
    """List of keys to mount into the container in the specified path.
    If None, all items will be mounted."""


class VolumeSecret(BaseModel):
    """
    Spec for secret volume.
    """
    mount_path: str
    """Volume mount path inside the container."""

    items: list[str] = None
    """List of keys to mount into the container in the specified path.
    If None, all items will be mounted."""


class VolumePVC(BaseModel):
    """
    Spec for persistent volume claim volume.
    """
    mount_path: str
    """Volume mount path inside the container."""


class NodeSelector(BaseModel):
    """
    NodeSelector model.
    """

    key: str
    """Node selector key."""

    value: str
    """Node selector value."""


class Resource(BaseModel):
    """
    Resource model.
    """

    resource_type: Literal["cpu", "memory", "gpu"]
    """Resource kind (cpu, memory, gpu)."""

    requests: int
    """Resource requests."""

    limits: int
    """Resource limits."""


class Env(BaseModel):
    """
    Env variable model.
    """

    name: str
    """Env variable name."""

    value: str
    """Env variable value."""


class K8sResources(BaseModel):
    """
    K8sResources model.
    """

    node_selector: NodeSelector = {}
    """Node selector."""

    volumes: list[Volume] = []
    """List of volumes."""

    resources: list[Resource] = []
    """Resources restrictions."""

    env: list[Env] = []
    """Env variables."""

    secrets: list[str] = []
    """List of secret names."""
