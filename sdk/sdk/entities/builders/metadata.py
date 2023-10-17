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
from sdk.utils.generic_utils import get_timestamp

if typing.TYPE_CHECKING:
    from sdk.entities.base.metadata import Metadata


class MetadataBuilder(dict):
    """
    Metadata builder class.
    """

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
        self[module] = metadata

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
        if module not in self:
            raise ValueError(f"Invalid module name: {module}")
        kwargs = self._parse_arguments(**kwargs)
        return self[module](**kwargs)

    @staticmethod
    def _parse_arguments(**kwargs) -> dict:
        """
        Parse keyword arguments and add default values.

        Parameters
        ----------
        **kwargs
            Keyword arguments.

        Returns
        -------
        dict
            A dictionary containing the entity metadata attributes.
        """
        if "created" not in kwargs or kwargs["created"] is None:
            kwargs["created"] = get_timestamp()
        if "updated" not in kwargs or kwargs["updated"] is None:
            kwargs["updated"] = kwargs["created"]
        return kwargs


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
