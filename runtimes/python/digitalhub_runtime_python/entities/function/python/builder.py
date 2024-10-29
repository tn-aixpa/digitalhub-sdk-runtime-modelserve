from __future__ import annotations

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderPython
from digitalhub_runtime_python.entities.function.python.entity import FunctionPython
from digitalhub_runtime_python.entities.function.python.spec import FunctionSpecPython, FunctionValidatorPython
from digitalhub_runtime_python.entities.function.python.status import FunctionStatusPython
from digitalhub_runtime_python.entities.function.python.utils import source_check, source_post_check

from digitalhub.entities.function._base.builder import FunctionBuilder


class FunctionPythonBuilder(FunctionBuilder, RuntimeEntityBuilderPython):
    """
    FunctionPython builder.
    """

    ENTITY_CLASS = FunctionPython
    ENTITY_SPEC_CLASS = FunctionSpecPython
    ENTITY_SPEC_VALIDATOR = FunctionValidatorPython
    ENTITY_STATUS_CLASS = FunctionStatusPython
    ENTITY_KIND = "python"

    def build(
        self,
        kind: str,
        project: str,
        name: str,
        uuid: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = False,
        **kwargs,
    ) -> FunctionPython:
        kwargs = source_check(**kwargs)
        obj = super().build(
            kind,
            project,
            name,
            uuid,
            description,
            labels,
            embedded,
            **kwargs,
        )
        return source_post_check(obj)
