from __future__ import annotations

from digitalhub.entities._builders.entity import EntityBuilder
from digitalhub.entities.project.project.entity import Project
from digitalhub.entities.project.project.spec import ProjectSpec, ProjectValidator
from digitalhub.entities.project.project.status import ProjectStatus


class ProjectProjectBuilder(EntityBuilder):
    """
    ProjectProject builder.
    """

    ENTITY_CLASS = Project
    ENTITY_SPEC_CLASS = ProjectSpec
    ENTITY_SPEC_VALIDATOR = ProjectValidator
    ENTITY_STATUS_CLASS = ProjectStatus

    def build(
        self,
        name: str,
        kind: str,
        description: str | None = None,
        labels: list[str] | None = None,
        local: bool = False,
        context: str | None = None,
        **kwargs,
    ) -> Project:
        """
        Create a new object.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        local : bool
            If True, use local backend, if False use DHCore backend. Default to False.
        context : str
            The context local folder of the project.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Project
            Object instance.
        """
        name = self.build_name(name)
        metadata = self.build_metadata(
            project=name,
            name=name,
            description=description,
            labels=labels,
        )
        spec = self.build_spec(
            self.ENTITY_SPEC_CLASS,
            self.ENTITY_SPEC_VALIDATOR,
            context=context,
            **kwargs,
        )
        status = self.build_status(self.ENTITY_STATUS_CLASS)
        return self.ENTITY_CLASS(
            name=name,
            kind=kind,
            metadata=metadata,
            spec=spec,
            status=status,
            local=local,
        )
