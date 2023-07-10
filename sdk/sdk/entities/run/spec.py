"""
Run spec module.
"""
from sdk.entities.base.spec import EntitySpec


class RunSpec(EntitySpec):
    """
    Run specification.
    """

    def __init__(
        self,
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

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__:
                self.__setattr__(k, v)
