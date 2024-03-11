"""
Base Function specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.spec import Spec, SpecParams


class FunctionSpec(Spec):
    """
    Specification for a Function.
    """

    def __init__(
        self,
        source: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        source : str
            Path to the Function's source code on the local file system.
        **kwargs
            Keyword arguments.
        """
        self.source = source

        self._any_setter(**kwargs)


class FunctionParams(SpecParams):
    """
    Function parameters model.
    """

    source: str = None
    """Path to the Function's source code on the local file system."""


class SourceCodeStruct:
    """
    Source code struct.
    """

    def __init__(
        self, source_code: str | None = None, source_encoded: str | None = None, lang: str | None = None
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        source_code : str
            Source code.
        source_encoded : str
            Base64 encoded source code.
        lang : str
            Code language.
        """
        self.source_code = source_code
        self.source_encoded = source_encoded
        self.lang = lang

    def to_dict(self) -> dict:
        """
        Convert to dictionary.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        return {
            "source_encoded": self.source_encoded,
            "lang": self.lang,
        }
