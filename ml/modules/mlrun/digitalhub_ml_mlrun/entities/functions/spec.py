"""
Job Function specification module.
"""
from __future__ import annotations

from pathlib import Path

from digitalhub_core.entities.functions.spec import FunctionParams, FunctionSpec, SourceCodeStruct
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import decode_string, encode_source


class FunctionSpecMlrun(FunctionSpec):
    """
    Specification for a Function job.
    """

    def __init__(
        self,
        source: dict,
        image: str | None = None,
        tag: str | None = None,
        handler: str | None = None,
        command: str | None = None,
        requirements: list | None = None,
    ) -> None:
        """
        Constructor.
        """
        super().__init__()

        self.image = image
        self.tag = tag
        self.handler = handler
        self.command = command
        self.requirements = requirements if requirements is not None else []

        self._source_check(source)
        self.source = SourceCodeStruct(**source)

    @staticmethod
    def _source_check(source: dict) -> dict:
        """
        Check source.

        Parameters
        ----------
        source : dict
            Source.

        Returns
        -------
        dict
            Checked source.
        """
        if source is None:
            raise EntityError("Source must be provided.")

        # Source check
        source_path = str(source.get("source"))
        code = str(source.get("code"))
        base64 = str(source.get("base64"))

        if source_path is None and code is None and base64 is None:
            raise EntityError("Source must be provided.")

        if base64 is not None:
            if code is None:
                source["code"] = decode_string(base64)
            return source

        if source_path is not None:
            if not (Path(source_path).suffix == ".py" and Path(source_path).is_file()):
                raise EntityError("Source is not a valid python file.")

            if base64 is None:
                source["base64"] = encode_source(source_path)

            if code is None:
                source["code"] = Path(source_path).read_text()

        return source

    def show_source_code(self) -> str:
        """
        Show source code.

        Returns
        -------
        str
            Source code.
        """
        if self.source.code is None:
            return ""
        return self.source.code

    def to_dict(self) -> dict:
        """
        Override to_dict to exclude code from source.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        dict_ = super().to_dict()
        dict_["source"] = self.source.to_dict()
        return dict_


class FunctionParamsMlrun(FunctionParams):
    """
    Function mlrun parameters model.
    """

    source: dict
    "Source code"

    image: str = None
    "Container image name"

    tag: str = None
    "Container image tag"

    handler: str = None
    "Handler method inside the function"

    command: str = None
    "Override the command run in the container"

    requirements: list = None
    "Requirements list, as used by the runtime"
