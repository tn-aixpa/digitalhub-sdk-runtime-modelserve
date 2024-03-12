"""
Job Function specification module.
"""
from __future__ import annotations

from pathlib import Path

from digitalhub_core.entities.functions.spec import FunctionParams, FunctionSpec, SourceCodeStruct
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import encode_source


class FunctionSpecMlrun(FunctionSpec):
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
        image : str
            Name of the Function's container image.
        tag : str
            Tag of the Function's container image.
        handler : str
            Function handler name.
        command : str
            Command to run inside the container.
        requirements : list
            List of requirements for the Function.
        """
        super().__init__(source, **kwargs)

        self.image = image
        self.tag = tag
        self.handler = handler
        self.command = command
        self.requirements = requirements if requirements is not None else []

        build = kwargs.get("build")
        if build is not None or build:
            self.build = SourceCodeStruct(**build)
        else:
            # Source check
            if source is None:
                raise EntityError("Source must be provided.")
            if not (Path(source).suffix == ".py" and Path(source).is_file()):
                raise EntityError("Source is not a valid python file.")
            self.build = SourceCodeStruct(
                source_code=Path(source).read_text(),
                source_encoded=encode_source(source),
                lang="python",
            )

    def show_source_code(self) -> str:
        """
        Show source code.

        Returns
        -------
        str
            Source code.
        """
        return str(self.build.source_code)

    def to_dict(self) -> dict:
        """
        Override to_dict to exclude build source_code.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        dict_ = super().to_dict()
        dict_["build"] = self.build.to_dict()
        return dict_


class FunctionParamsMlrun(FunctionParams):
    """
    Function mlrun parameters model.
    """

    image: str = None
    """Name of the Function's container image."""

    tag: str = None
    """Tag of the Function's container image."""

    handler: str = None
    """Function handler name."""

    command: str = None
    """Command to run inside the container."""

    requirements: list = None
    """List of requirements for the Function."""
