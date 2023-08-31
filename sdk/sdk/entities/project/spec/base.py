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
        functions: list[dict] | None = None,
        artifacts: list[dict] | None = None,
        workflows: list[dict] | None = None,
        dataitems: list[dict] | None = None,
    ) -> None:
        """
        Initializes a new instance of the ProjectSpec class.

        Parameters
        ----------
        context : str
            The context of the project.
        source : str
            The source of the project.
        functions : list[dict]
            A list of dictionaries representing the functions in the project.
        artifacts : list[dict]
            A list of dictionaries representing the artifacts in the project.
        workflows : list[dict]
            A list of dictionaries representing the workflows in the project.
        dataitems : list[dict]
            A list of dictionaries representing the data items in the project.

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
