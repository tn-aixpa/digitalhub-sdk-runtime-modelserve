"""
Job Function specification module.
"""
from sdk.entities.function.spec.base import FunctionSpec
from sdk.entities.utils.utils import encode_source
from sdk.utils.exceptions import EntityError
from sdk.utils.file_utils import is_python_module
from sdk.utils.uri_utils import get_name_from_uri


class FunctionSpecJob(FunctionSpec):
    """
    Specification for a Function job.
    """

    def __init__(
        self,
        source: str | None = None,
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
        """
        super().__init__(
            source,
            image,
            tag,
            handler,
            command,
            **kwargs,
        )
        if source is None:
            raise EntityError("Source must be provided.")

        if not is_python_module(source):
            raise EntityError("Source is not a valid python file.")

        self.requirements = requirements if requirements is not None else []
        self.build = {
            "functionSourceCode": encode_source(source),
            "code_origin": source,
            "origin_filename": get_name_from_uri(source),
        }
