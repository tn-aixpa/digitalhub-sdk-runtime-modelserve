from __future__ import annotations

from typing import Literal

from digitalhub_runtime_python.entities.function.python.models import SourceValidator

from digitalhub.entities.function._base.spec import FunctionSpec, FunctionValidator


class FunctionSpecPython(FunctionSpec):
    """
    FunctionSpecPython specifications.
    """

    def __init__(
        self,
        source: dict | None = None,
        image: str | None = None,
        base_image: str | None = None,
        python_version: str | None = None,
        requirements: list | None = None,
    ) -> None:
        super().__init__()

        self.image = image
        self.base_image = base_image
        self.python_version = python_version
        self.requirements = requirements
        self.source = source


class FunctionValidatorPython(FunctionValidator):
    """
    FunctionValidatorPython validator.
    """

    source: SourceValidator = None
    """Source code validator"""

    python_version: Literal["PYTHON3_9", "PYTHON3_10", "PYTHON3_11"]
    "Python version"

    image: str = None
    "Image where the function will be executed"

    base_image: str = None
    "Base image used to build the image where the function will be executed"

    requirements: list = None
    "Requirements list to be installed in the image where the function will be executed"
