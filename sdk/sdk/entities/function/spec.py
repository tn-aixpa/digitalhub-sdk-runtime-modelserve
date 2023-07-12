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
        source: str = None,
        image: str = None,
        tag: str = None,
        handler: str = None,
        command: str = None,
        requirements: list = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        source : str, optional
            Path to the Function's source code on the local file system.
        image : str, optional
            Name of the Function's container image.
        tag : str, optional
            Tag of the Function's container image.
        handler : str, optional
            Function handler name.
        command : str, optional
            Command to run inside the container.
        requirements : list, optional
            List of requirements for the Function.

        """
        self.source = source
        self.image = image
        self.tag = tag
        self.handler = handler
        self.command = command
        self.requirements = requirements if requirements is not None else []

        self._any_setter(**kwargs)


class FunctionSpecJob(FunctionSpec):
    """
    Specification for a Function job.
    """

    def __init__(
        self,
        source: str = None,
        image: str = None,
        tag: str = None,
        handler: str = None,
        command: str = None,
        requirements: list = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

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
            requirements,
            **kwargs,
        )
        if not is_python_module(source):
            warnings.warn("Source is not a valid python file.")

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
