"""
Dataitem spec module.
"""
from sdk.entities.base.spec import EntitySpec


class DataitemSpec(EntitySpec):
    """
    Dataitem specifications.
    """

    def __init__(self, key: str = None, path: str = None, **kwargs) -> None:
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
        self.key = key
        self.path = path

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__:
                self.__setattr__(k, v)
