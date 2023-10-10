"""
Task specification module.
"""
from sdk.entities.base.spec import EntitySpec


class TaskSpec(EntitySpec):
    """Task specification."""

    def __init__(self, function: str | None = None, **kwargs) -> None:
        """
        Constructor.

        Parameters
        ----------
        function : str
            Function string.
        **kwargs
            Keyword arguments.
        """
        self.function = function

        self._any_setter(**kwargs)
