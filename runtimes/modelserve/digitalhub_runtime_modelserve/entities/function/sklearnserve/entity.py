from __future__ import annotations

import typing

from digitalhub.entities.function._base.entity import Function

if typing.TYPE_CHECKING:
    from digitalhub_runtime_modelserve.entities.function.sklearnserve.spec import FunctionSpecSklearnserve
    from digitalhub_runtime_modelserve.entities.function.sklearnserve.status import FunctionStatusSklearnserve

    from digitalhub.entities._base.entity.metadata import Metadata


class FunctionSklearnserve(Function):
    """
    FunctionSklearnserve class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: FunctionSpecSklearnserve,
        status: FunctionStatusSklearnserve,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: FunctionSpecSklearnserve
        self.status: FunctionStatusSklearnserve
