from __future__ import annotations

from digitalhub_core.entities.function.spec import FunctionParams, FunctionSpec
from digitalhub_runtime_container.entities.function.models import SourceCodeParamsContainer, SourceCodeStructContainer


class FunctionSpecContainer(FunctionSpec):
    """
    Specification for a Function job.
    """

    def __init__(
        self,
        image: str | None = None,
        base_image: str | None = None,
        command: str | None = None,
        args: list[str] | None = None,
        source: dict | None = None,
        code_src: str | None = None,
        handler: str | None = None,
        code: str | None = None,
        base64: str | None = None,
        lang: str | None = None,
    ) -> None:
        super().__init__()

        self.image = image
        self.base_image = base_image
        self.command = command
        self.args = args

        self.source = self._set_source(source, code_src, handler, code, base64, lang)

    def _set_source(
        self,
        source: dict | None,
        code_src: str | None,
        handler: str | None,
        code: str | None,
        base64: str | None,
        lang: str | None,
    ) -> SourceCodeStructContainer | None:
        """
        Set source code.

        Parameters
        ----------
        source : dict
            Source code dictionary.
        code_src : str
            Source code reference.
        handler : str
            Function handler.
        code : str
            Source code.
        base64 : str
            Source code (base64 encoded).
        lang : str
            Source code language.

        Returns
        -------
        SourceCodeStruct
            Source code.
        """
        # Give source precedence
        if source is not None:
            source_dict = source
        else:
            source_dict = {
                "source": code_src,
                "handler": handler,
                "code": code,
                "base64": base64,
                "lang": lang,
            }

        # Check if some values are provided for source
        if any([True for i in source_dict.values() if i is not None]):
            source_checked = self.source_check(source_dict)
            self.source = SourceCodeStructContainer(**source_checked)
        else:
            self.source = None

    @staticmethod
    def source_check(source: dict) -> dict:
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
        return SourceCodeStructContainer.source_check(source)

    def show_source_code(self) -> str:
        """
        Show source code.

        Returns
        -------
        str
            Source code.
        """
        return self.source.show_source_code()

    def to_dict(self) -> dict:
        """
        Override to_dict to exclude code from source.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        dict_ = super().to_dict()
        if self.source is not None:
            dict_["source"] = self.source.to_dict()
        return dict_


class FunctionParamsContainer(FunctionParams, SourceCodeParamsContainer):
    """
    Function container parameters model.
    """

    image: str = None
    """Name of the Function's container image."""

    base_image: str = None
    """Function's base container image."""

    command: str = None
    """Command to run inside the container."""

    args: list[str] = None
    """Arguments to pass to the entrypoint."""
