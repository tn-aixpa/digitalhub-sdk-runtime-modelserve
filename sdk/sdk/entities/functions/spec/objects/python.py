"""
Python Function specification module.
"""
from sdk.entities.functions.spec.objects.base import FunctionParams, FunctionSpec
from sdk.utils.exceptions import EntityError
from sdk.utils.file_utils import is_python_module
from sdk.utils.generic_utils import encode_source
from sdk.utils.uri_utils import get_name_from_uri


class FunctionSpecPython(FunctionSpec):
    """
    Specification for a Function Python.
    """

    def __init__(
        self,
        source: str | None = None,
        handler: str | None = None,
        image: str | None = None,
        command: str | None = None,
        args: list | None = None,
        requirements: list | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        name : str
            Name of the Function.
        image : str
            Name of the Function's container image.
        command : str
            Command to run inside the container.
        args : list
            List of arguments for the command.
        requirements : list
            List of requirements for the Function.
        """
        super().__init__(source, **kwargs)
        if source is None:
            raise EntityError("Source must be provided.")

        if not is_python_module(source):
            raise EntityError("Source is not a valid python file.")

        if handler is None:
            raise EntityError("Function handler must be provided.")

        self.handler = handler
        self.image = image
        self.command = command
        self.args = args
        self.requirements = requirements if requirements is not None else []
        self.code = encode_source(source)


class FunctionParamsPython(FunctionParams):
    """
    Function Python parameters model.
    """

    handler: str
    """Name of the Function."""

    image: str
    """Name of the Function's container image."""

    command: str
    """Command to run inside the container."""

    args: list
    """List of arguments for the command."""

    requirements: list
    """List of requirements for the Function."""
