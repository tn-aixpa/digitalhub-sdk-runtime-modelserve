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
        image: str | None = None,
        tag: str | None = None,
        handler: str | None = None,
        command: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        source : str
            Path to the Function's source code on the local file system.
        image : str
            Name of the Function's container image.
        tag : str
            Tag of the Function's container image.
        handler : str
            Function handler name.
        command : str
            Command to run inside the container.

        """
        self.source = source
        self.image = image
        self.tag = tag
        self.handler = handler
        self.command = command

        self._any_setter(**kwargs)
