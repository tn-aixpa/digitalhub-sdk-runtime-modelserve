"""
Project spec module.
"""
from sdk.entities.base.spec import EntitySpec


class ProjectSpec(EntitySpec):
    """
    Project specification.
    """

    def __init__(
        self,
        context: str = None,
        source: str = None,
        functions: list[dict] = None,
        artifacts: list[dict] = None,
        workflows: list[dict] = None,
        dataitems: list[dict] = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        **kwargs
            Additional keyword arguments.

        Notes
        -----
        If some of the attributes are not in the signature,
        they will be added as new attributes.
        """
        self.context = context
        self.source = source
        self.functions = functions if functions is not None else []
        self.artifacts = artifacts if artifacts is not None else []
        self.workflows = workflows if workflows is not None else []
        self.dataitems = dataitems if dataitems is not None else []

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__:
                self.__setattr__(k, v)
