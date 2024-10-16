from __future__ import annotations

import typing

from digitalhub.entities.function._base.entity import Function

if typing.TYPE_CHECKING:
    from digitalhub_runtime_modelserve.entities.function.huggingfaceserve.spec import FunctionSpecHuggingfaceserve
    from digitalhub_runtime_modelserve.entities.function.huggingfaceserve.status import FunctionStatusHuggingfaceserve

    from digitalhub.entities._base.entity.metadata import Metadata


class FunctionHuggingfaceserve(Function):
    """
    FunctionHuggingfaceserve class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: FunctionSpecHuggingfaceserve,
        status: FunctionStatusHuggingfaceserve,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: FunctionSpecHuggingfaceserve
        self.status: FunctionStatusHuggingfaceserve
