"""
Project base specification module.
"""
from sdk.entities.base.spec import EntitySpec


class ProjectSpec(EntitySpec):
    """
    Project specification.
    """

    def __init__(
        self,
        context: str | None = None,
        source: str | None = None,
        functions: list | None = None,
        artifacts: list | None = None,
        workflows: list | None = None,
        dataitems: list | None = None,
    ) -> None:
        """
        Initializes a new instance of the ProjectSpec class.

        Parameters
        ----------
        context : str
            The project's context.

        source : str
            The project's source.

        functions : list
            List of project's functions.

        artifacts : list
            List of project's artifacts.

        workflows : list
            List of project's workflows.

        dataitems : list
            List of project's dataitems.

        Returns
        -------
        None
        """
        self.context = context
        self.source = source
        self.functions = functions if functions is not None else []
        self.artifacts = artifacts if artifacts is not None else []
        self.workflows = workflows if workflows is not None else []
        self.dataitems = dataitems if dataitems is not None else []
