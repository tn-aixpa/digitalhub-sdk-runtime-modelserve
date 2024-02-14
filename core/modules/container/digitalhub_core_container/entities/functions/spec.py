"""
Job Function specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.functions.spec import FunctionParams, FunctionSpec


class FunctionSpecContainer(FunctionSpec):
    """
    Specification for a Function job.
    """

    def __init__(
        self,
        source: str | None = None,
        image: str | None = None,
        base_image: str | None = None,
        command: str | None = None,
        entrypoint: str | None = None,
        args: list[str] | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        image : str
            Name of the Function's container image.
        base_image : str
            Function's base container image.
        command : str
            Command to run inside the container.
        entrypoint : str
            Entrypoint to run inside the container.
        args : list
            Arguments to pass to the entrypoint.
        """
        super().__init__(source, **kwargs)

        self.image = image
        self.base_image = base_image
        self.command = command
        self.entrypoint = entrypoint
        self.args = args


class FunctionParamsContainer(FunctionParams):
    """
    Function container parameters model.
    """

    image: str
    """Name of the Function's container image."""

    base_image: str = None
    """Function's base container image."""

    command: str = None
    """Command to run inside the container."""

    entrypoint: str = None
    """Entrypoint to run inside the container."""

    args: list[str] = None
    """Arguments to pass to the entrypoint."""


spec_registry = {
    "container": [FunctionSpecContainer, FunctionParamsContainer],
}
