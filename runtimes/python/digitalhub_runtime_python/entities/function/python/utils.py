from __future__ import annotations

import typing
from pathlib import Path

from digitalhub.stores.api import get_store
from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.file_utils import eval_py_type, eval_zip_type
from digitalhub.utils.generic_utils import encode_source, encode_string
from digitalhub.utils.s3_utils import get_s3_bucket
from digitalhub.utils.uri_utils import map_uri_scheme

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.function.python.entity import FunctionPython


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
    source: dict = kwargs.pop("source", {})
    source.update(
        {
            "source": kwargs.pop("code_src", source.get("source")),
            "code": kwargs.pop("code", source.get("code")),
            "base64": kwargs.pop("base64", source.get("base64")),
            "handler": kwargs.pop("handler", source.get("handler")),
            "init_function": kwargs.pop("init_function", source.get("init_function")),
            "lang": kwargs.pop("lang", source.get("lang")),
        }
    )
    kwargs["source"] = _check_params(**source)
    return kwargs


def _check_params(
    code_src: str | None = None,
    code: str | None = None,
    base64: str | None = None,
    handler: str | None = None,
    init_function: str | None = None,
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
    init_function : str
        Init function.
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

    if init_function is not None:
        source["init_function"] = init_function

    if lang is None:
        source["lang"] = "python"

    if code_src is None and code is None and base64 is None:
        raise EntityError("Source must be provided.")

    if code_src is not None:
        source["source"] = code_src

    if base64 is not None:
        source["base64"] = base64

    if code is not None:
        source["base64"] = encode_string(code)

    return source


def source_post_check(exec: FunctionPython) -> FunctionPython:
    """
    Post check source.

    Parameters
    ----------
    exec : FunctionPython
        Executable.

    Returns
    -------
    FunctionPython
        Updated executable.
    """
    code_src = exec.spec.source.get("source", None)
    base64 = exec.spec.source.get("base64", None)
    if code_src is None or base64 is not None:
        return exec

    # Check local source
    if map_uri_scheme(code_src) == "local" and Path(code_src).is_file():
        # Check py
        if eval_py_type(code_src):
            exec.spec.source["base64"] = encode_source(code_src)

        # Check zip
        elif eval_zip_type(code_src):
            filename = Path(code_src).name
            dst = f"zip+s3://{get_s3_bucket()}/{exec.project}/{exec.ENTITY_TYPE}/{exec.name}/{exec.id}/{filename}"
            get_store(dst).upload(code_src, dst)
            exec.spec.source["source"] = dst
            if ":" not in exec.spec.source["handler"]:
                exec.spec.source["handler"] = f"{Path(code_src).stem}:{exec.spec.source['handler']}"

    return exec
