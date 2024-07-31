from __future__ import annotations

from pathlib import Path

from digitalhub_core.entities.function.models import SourceCodeParams, SourceCodeStruct
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import encode_source, encode_string
from digitalhub_core.utils.uri_utils import map_uri_scheme


class SourceCodeStructContainer(SourceCodeStruct):
    """
    Source code struct for container.
    """

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
        # Source check
        source_path = source.get("source")
        code = source.get("code")
        base64 = source.get("base64")
        handler = source.get("handler")

        if source_path is None and code is None and base64 is None:
            raise EntityError("Source must be provided.")

        if base64 is not None:
            return source

        if code is not None:
            source["base64"] = encode_string(code)
            return source

        if source_path is not None:
            if map_uri_scheme(source_path) == "local":
                if not Path(source_path).exists():
                    raise EntityError("Source does not exist.")
                source["base64"] = encode_source(source_path)
            else:
                if handler is None:
                    raise EntityError("Handler must be provided if source is not local.")

        return source


class SourceCodeParamsContainer(SourceCodeParams):
    """
    Source code params for container.
    """
