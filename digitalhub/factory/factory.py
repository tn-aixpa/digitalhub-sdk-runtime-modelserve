from __future__ import annotations

import typing

from digitalhub.utils.exceptions import BuilderError

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.entity import Entity
    from digitalhub.entities._base.entity.metadata import Metadata
    from digitalhub.entities._base.entity.spec import Spec
    from digitalhub.entities._base.entity.status import Status
    from digitalhub.entities._builders.entity import EntityBuilder
    from digitalhub.runtimes._base import Runtime
    from digitalhub.runtimes.builder import RuntimeBuilder


class Factory:
    """
    Factory class for building entities and runtimes.
    """

    def __init__(self):
        self._entity_builders: dict[str, EntityBuilder] = {}
        self._runtime_builders: dict[str, RuntimeBuilder] = {}

    def add_entity_builder(self, name: str, builder: EntityBuilder) -> None:
        """
        Add a builder to the factory.

        Parameters
        ----------
        name : str
            Builder name.
        builder : EntityBuilder
            Builder object.

        Returns
        -------
        None
        """
        if name in self._entity_builders:
            raise BuilderError(f"Builder {name} already exists.")
        self._entity_builders[name] = builder()

    def add_runtime_builder(self, name: str, builder: RuntimeBuilder) -> None:
        """
        Add a builder to the factory.

        Parameters
        ----------
        name : str
            Builder name.
        builder : RuntimeBuilder
            Builder object.

        Returns
        -------
        None
        """
        if name in self._runtime_builders:
            raise BuilderError(f"Builder {name} already exists.")
        self._runtime_builders[name] = builder()

    def build_entity_from_params(self, kind_to_build_from: str, *args, **kwargs) -> Entity:
        """
        Build an entity.

        Parameters
        ----------
        kind_to_build_from : str
            Entity type.

        Returns
        -------
        Entity
            Entity object.
        """
        self._raise_if_builder_not_found(kind_to_build_from)
        return self._entity_builders[kind_to_build_from].build(*args, **kwargs)

    def build_entity_from_dict(self, kind_to_build_from: str, dict_data: dict) -> Entity:
        """
        Build an entity from a dictionary.

        Parameters
        ----------
        kind_to_build_from : str
            Entity type.
        dict_data : dict
            Dictionary with entity data.

        Returns
        -------
        Entity
            Entity object.
        """
        self._raise_if_builder_not_found(kind_to_build_from)
        return self._entity_builders[kind_to_build_from].from_dict(dict_data)

    def build_spec(self, kind_to_build_from: str, **kwargs) -> Spec:
        """
        Build an entity spec.

        Parameters
        ----------
        kind_to_build_from : str
            Entity type.

        Returns
        -------
        Spec
            Spec object.
        """
        self._raise_if_builder_not_found(kind_to_build_from)
        return self._entity_builders[kind_to_build_from].build_spec(**kwargs)

    def build_metadata(self, kind_to_build_from: str, **kwargs) -> Metadata:
        """
        Build an entity metadata.

        Parameters
        ----------
        kind_to_build_from : str
            Entity type.

        Returns
        -------
        Metadata
            Metadata object.
        """
        self._raise_if_builder_not_found(kind_to_build_from)
        return self._entity_builders[kind_to_build_from].build_metadata(**kwargs)

    def build_status(self, kind_to_build_from: str, **kwargs) -> Status:
        """
        Build an entity status.

        Parameters
        ----------
        kind_to_build_from : str
            Entity type.

        Returns
        -------
        Status
            Status object.
        """
        self._raise_if_builder_not_found(kind_to_build_from)
        return self._entity_builders[kind_to_build_from].build_status(**kwargs)

    def build_runtime(self, kind_to_build_from: str, project: str) -> Runtime:
        """
        Build a runtime.

        Parameters
        ----------
        kind_to_build_from : str
            Runtime type.
        project : str
            Project name.

        Returns
        -------
        Runtime
            Runtime object.
        """
        self._raise_if_builder_not_found(kind_to_build_from)
        return self._runtime_builders[kind_to_build_from].build(project=project)

    def get_entity_type_from_builder(self, kind: str) -> str:
        """
        Get entity type from builder.

        Parameters
        ----------
        kind : str
            Entity type.

        Returns
        -------
        str
            Entity type.
        """
        self._raise_if_builder_not_found(kind)
        return self._entity_builders[kind].ENTITY_TYPE

    def _raise_if_builder_not_found(self, kind: str) -> None:
        """
        Raise error if builder not found.

        Parameters
        ----------
        kind : str
            Entity type.

        Returns
        -------
        None
        """
        if kind not in self._entity_builders:
            raise BuilderError(f"Builder for kind '{kind}' not found.")


factory = Factory()
