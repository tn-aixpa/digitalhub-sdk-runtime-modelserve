"""
Metadata factory module.
"""
from __future__ import annotations

import typing

from sdk.entities.artifacts.metadata import ArtifactMetadata
from sdk.entities.dataitems.metadata import DataitemMetadata
from sdk.entities.functions.metadata import FunctionMetadata
from sdk.entities.projects.metadata import ProjectMetadata
from sdk.entities.runs.metadata import RunMetadata
from sdk.entities.tasks.metadata import TaskMetadata
from sdk.entities.workflows.metadata import WorkflowMetadata
from sdk.utils.commons import ARTF, DTIT, FUNC, PROJ, RUNS, TASK, WKFL

if typing.TYPE_CHECKING:
    from sdk.entities.base.metadata import Metadata


class MetadataBuilder:
    """
    Metadata factory class.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._modules = {}

    def register(self, module: str, metadata: Metadata) -> None:
        """
        Register metadata.

        Parameters
        ----------
        module: str
            module name.
        metadata: Metadata
            Metadata object.

        Returns
        -------
        None
        """
        self._modules[module] = metadata

    def build(self, module: str, **kwargs) -> Metadata:
        """
        Build entity metadata object.

        Parameters
        ----------
        module: str
            module name.
        **kwargs
            Keyword arguments.

        Returns
        -------
        Metadata
            An entity metadata object.
        """
        if module not in self._modules:
            raise ValueError(f"Invalid module name: {module}")
        return self._modules[module](**kwargs)


def build_metadata(module: str, **kwargs) -> Metadata:
    """
    Wrapper for MetadataBuilder.build_metadata.

    Parameters
    ----------
    module: str
        Module name.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Metadata
        An entity metadata object.
    """
    return metadata_builder.build(module, **kwargs)


metadata_builder = MetadataBuilder()
metadata_builder.register(ARTF, ArtifactMetadata)
metadata_builder.register(DTIT, DataitemMetadata)
metadata_builder.register(FUNC, FunctionMetadata)
metadata_builder.register(PROJ, ProjectMetadata)
metadata_builder.register(RUNS, RunMetadata)
metadata_builder.register(TASK, TaskMetadata)
metadata_builder.register(WKFL, WorkflowMetadata)
