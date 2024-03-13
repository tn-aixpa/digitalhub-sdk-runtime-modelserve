"""
Dbt Function specification module.
"""
from __future__ import annotations

from pathlib import Path

from digitalhub_core.entities.functions.spec import FunctionParams, FunctionSpec, SourceCodeStruct
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import decode_string, encode_string


class FunctionSpecDbt(FunctionSpec):
    """
    Specification for a Function Dbt.
    """

    def __init__(self, source: dict) -> None:
        """
        Constructor.

        Parameters
        ----------
        sql : str
            SQL query to run inside Dbt.
        """
        super().__init__()

        source = self._check_source(source)
        self.source = SourceCodeStruct(**source)

    @staticmethod
    def _check_source(source: dict) -> dict:
        """
        Check source code.

        Parameters
        ----------
        source : dict
            Source.

        Returns
        -------
        dict
            Checked source.
        """
        source_path = source.get("source")
        code = source.get("code")
        base64 = source.get("base64")

        if not source_path and not code and not base64:
            raise EntityError("Source code must be provided.")

        if code is not None:
            source["base64"] = encode_string(code)

        if base64 is not None:
            try:
                source["code"] = decode_string(base64)
            except Exception:
                ...

        if source_path is not None:
            try:
                source["code"] = Path(source_path).read_text()
                source["base64"] = encode_string(source["code"])
            except Exception:
                raise EntityError("Cannot access source code.")

        return source

    def show_source_code(self) -> str:
        """
        Show source code.

        Returns
        -------
        str
            Source code.
        """
        if self.source is None:
            return ""
        return str(self.source.code)

    def to_dict(self) -> dict:
        """
        Override to_dict to exclude sql source_code.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        dict_ = super().to_dict()
        dict_["source"] = self.source.to_dict()
        return dict_


class FunctionParamsDbt(FunctionParams):
    """
    Function Dbt parameters model.
    """

    source: dict
    """Source code."""
