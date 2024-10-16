from __future__ import annotations

import typing

from digitalhub.entities._builders.entity import EntityBuilder

if typing.TYPE_CHECKING:
    from digitalhub.entities.task._base.entity import Task


class TaskBuilder(EntityBuilder):
    """
    Task builder.
    """

    def build(
        self,
        project: str,
        kind: str,
        uuid: str | None = None,
        labels: list[str] | None = None,
        function: str | None = None,
        **kwargs,
    ) -> Task:
        """
        Create a new object.

        Parameters
        ----------
        project : str
            Project name.
        kind : str
            Kind the object.
        uuid : str
            ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
        labels : list[str]
            List of labels.
        function : str
            Name of the executable associated with the task.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Task
            Object instance.
        """
        uuid = self.build_uuid(uuid)
        metadata = self.build_metadata(
            project=project,
            name=uuid,
            labels=labels,
        )
        spec = self.build_spec(
            self.ENTITY_SPEC_CLASS,
            self.ENTITY_SPEC_VALIDATOR,
            function=function,
            **kwargs,
        )
        status = self.build_status(self.ENTITY_STATUS_CLASS)
        return self.ENTITY_CLASS(
            project=project,
            uuid=uuid,
            kind=kind,
            metadata=metadata,
            spec=spec,
            status=status,
        )
