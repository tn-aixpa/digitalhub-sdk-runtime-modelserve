from __future__ import annotations

import typing

from digitalhub_core.context.builder import get_context
from digitalhub_core.entities._base.crud import create_entity_api_ctx, read_entity_api_ctx, update_entity_api_ctx
from digitalhub_core.entities._base.entity.base import Entity
from digitalhub_core.utils.generic_utils import get_timestamp

if typing.TYPE_CHECKING:
    from digitalhub_core.context.context import Context
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities._base.spec.base import Spec
    from digitalhub_core.entities._base.status.base import Status


class ContextEntity(Entity):
    def __init__(
        self,
        project: str,
        kind: str,
        metadata: Metadata,
        spec: Spec,
        status: Status,
        user: str | None = None,
    ) -> None:
        super().__init__(kind, metadata, spec, status, user)
        self.project = project
        self._obj_attr.extend(["project"])

    ##############################
    #  Save / Refresh / Export
    ##############################

    def save(self, update: bool = False) -> ContextEntity:
        """
        Save or update the entity into the backend.

        Parameters
        ----------
        update : bool
            Flag to indicate update.

        Returns
        -------
        ContextEntity
            Entity saved.
        """
        obj = self.to_dict()
        if not update:
            return self._save(obj)
        return self._update(obj)

    def _save(self, obj: dict) -> ContextEntity:
        """
        Save entity into backend.

        Parameters
        ----------
        obj : dict
            Object instance as dictionary.

        Returns
        -------
        ContextEntity
            Entity saved.
        """
        new_obj = create_entity_api_ctx(self.project, self.ENTITY_TYPE, obj)
        self._update_attributes(new_obj)
        return self

    def _update(self, obj: dict) -> ContextEntity:
        """
        Update entity in backend.

        Parameters
        ----------
        obj : dict
            Object instance as dictionary.

        Returns
        -------
        ContextEntity
            Entity updated.
        """
        if self._context().local:
            self.metadata.updated = obj["metadata"]["updated"] = get_timestamp()
        new_obj = update_entity_api_ctx(self.project, self.ENTITY_TYPE, self.id, obj)
        self._update_attributes(new_obj)
        return self

    def refresh(self) -> ContextEntity:
        """
        Refresh object from backend.

        Returns
        -------
        ContextEntity
            Entity refreshed.
        """
        new_obj = read_entity_api_ctx(self.key)
        self._update_attributes(new_obj)
        return self

    ##############################
    #  Context
    ##############################

    def _context(self) -> Context:
        """
        Get context.

        Returns
        -------
        Context
            Context object.
        """
        return get_context(self.project)
