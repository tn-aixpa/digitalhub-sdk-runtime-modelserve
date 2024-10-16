from __future__ import annotations

import typing

from digitalhub.entities._builders.entity import EntityBuilder

if typing.TYPE_CHECKING:
    from digitalhub.entities.workflow._base.entity import Workflow


class WorkflowBuilder(EntityBuilder):
    """
    Workflow builder.
    """

    def build(
        self,
        kind: str,
        project: str,
        name: str,
        uuid: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = True,
        **kwargs,
    ) -> Workflow:
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
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object spec must be embedded in project spec.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Workflow
            Object instance.
        """
        name = self.build_name(name)
        uuid = self.build_uuid(uuid)
        metadata = self.build_metadata(
            project=project,
            name=name,
            description=description,
            labels=labels,
        )
        spec = self.build_spec(
            self.ENTITY_SPEC_CLASS,
            self.ENTITY_SPEC_VALIDATOR,
            **kwargs,
        )
        status = self.build_status(self.ENTITY_STATUS_CLASS)
        return self.ENTITY_CLASS(
            project=project,
            name=name,
            uuid=uuid,
            kind=kind,
            metadata=metadata,
            spec=spec,
            status=status,
        )
