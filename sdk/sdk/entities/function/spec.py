"""
Function spec module.
"""
from sdk.entities.base.spec import EntitySpec
from sdk.utils.file_utils import is_python_module
from sdk.utils.uri_utils import get_name_from_uri
from sdk.utils.utils import encode_source
from sdk.utils.exceptions import EntityError


class FunctionSpec(EntitySpec):
    """
    Function specification.
    """

    def __init__(
        self,
        source: str,
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
        **kwargs
            Additional keyword arguments.

        Notes
        -----
        If some of the attributes are not in the signature,
        they will be added as new attributes.
        """
        self.source = source
        self.image = image
        self.tag = tag
        self.handler = handler
        self.command = command
        self.requirements = requirements if requirements is not None else []

        if not is_python_module(self.source):
            raise EntityError("Source is not a valid python file.")

        self.build = {
            "functionSourceCode": encode_source(source),
            "code_origin": source,
            "origin_filename": get_name_from_uri(source),
        }

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self.__dict__:
                self.__setattr__(k, v)
