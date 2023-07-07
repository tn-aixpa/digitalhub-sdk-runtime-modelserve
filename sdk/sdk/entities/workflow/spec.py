"""
Workflow spec module.
"""
from sdk.entities.base.spec import EntitySpec


class WorkflowSpec(EntitySpec):
    """
    Workflow specifications.
    """

    def __init__(self, test: str = None, **kwargs) -> None:
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
        self.test = test

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__:
                self.__setattr__(k, v)
