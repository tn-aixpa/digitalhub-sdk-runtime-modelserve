"""
Function spec module.
"""
import warnings

from sdk.entities.base.spec import EntitySpec
from sdk.utils.file_utils import is_python_module
from sdk.utils.uri_utils import get_name_from_uri
from sdk.entities.utils.utils import encode_source


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


class FunctionSpecJob(FunctionSpec):
    """
    Specification for a Function job.
    """

    def __init__(
        self,
        source: str = "",
        image: str | None = None,
        tag: str | None = None,
        handler: str | None = None,
        command: str | None = None,
        requirements: list | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        requirements : list
            List of requirements for the Function.

        See Also
        --------
        FunctionSpec.__init__

        """
        super().__init__(
            source,
            image,
            tag,
            handler,
            command,
            **kwargs,
        )

        if not is_python_module(source):
            warnings.warn("Source is not a valid python file.")

        self.requirements = requirements if requirements is not None else []
        self.build = {
            "functionSourceCode": encode_source(source),
            "code_origin": source,
            "origin_filename": get_name_from_uri(source),
        }


def build_spec(kind: str, **kwargs) -> FunctionSpec:
    """
    Build a FunctionSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of FunctionSpec to build.
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    FunctionSpec
        A FunctionSpec object with the given parameters.

    Raises
    ------
    ValueError
        If the given kind is not supported.
    """
    if kind == "job":
        return FunctionSpecJob(**kwargs)
    raise ValueError(f"Unknown kind: {kind}")
