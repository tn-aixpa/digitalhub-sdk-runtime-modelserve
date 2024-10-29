from __future__ import annotations

from pathlib import Path

from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.generic_utils import encode_source, encode_string
from digitalhub.utils.uri_utils import map_uri_scheme


def source_check(**kwargs) -> dict:
    """
    Check source code.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    dict
        Checked source.
    """
    source = kwargs.pop("source", None)
    code_src = kwargs.pop("code_src", None)
    code = kwargs.pop("code", None)
    base64 = kwargs.pop("base64", None)
    handler = kwargs.pop("handler", None)
    lang = kwargs.pop("lang", None)

    if source is not None:
        kwargs["source"] = source
    else:
        kwargs["source"] = _check_params(
            code_src=code_src,
            code=code,
            base64=base64,
            handler=handler,
            lang=lang,
        )
    return kwargs


def _check_params(
    code_src: str | None = None,
    code: str | None = None,
    base64: str | None = None,
    handler: str | None = None,
    lang: str | None = None,
) -> dict:
    """
    Check source.

    Parameters
    ----------
    code_src : str
        Source code source.
    code : str
        Source code.
    base64 : str
        Source code base64.
    handler : str
        Function handler.
    lang : str
        Source code language.

    Returns
    -------
    dict
        Checked source.
    """
    source = {}

    if handler is None:
        raise EntityError("Handler must be provided.")
    source["handler"] = handler

    if lang is None:
        source["lang"] = "python"

    if code_src is None and code is None and base64 is None:
        raise EntityError("Source must be provided.")

    if base64 is not None:
        source["base64"] = base64
        return source

    if code is not None:
        source["base64"] = encode_string(code)
        return source

    if code_src is not None:
        if map_uri_scheme(code_src) == "local":
            if not (Path(code_src).suffix == ".py" and Path(code_src).is_file()):
                raise EntityError("Source is not a valid python file.")
            source["base64"] = encode_source(code_src)
            return source

    raise EntityError("Local code_src must be provided.")
