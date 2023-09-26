"""
Base Function specification module.
"""
from sdk.entities.base.spec import EntitySpec


class FunctionSpec(EntitySpec):
    """
    Specification for a Function.
    """

    def __init__(
        self,
        source: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        source : str
            Path to the Function's source code on the local file system.
        **kwargs
            Keyword arguments.
        """
        self.source = source

        self._any_setter(**kwargs)
