from __future__ import annotations

from digitalhub_runtime_container.entities._base.runtime_entity.builder import RuntimeEntityBuilderContainer
from digitalhub_runtime_container.entities.function.container.entity import FunctionContainer
from digitalhub_runtime_container.entities.function.container.spec import (
    FunctionSpecContainer,
    FunctionValidatorContainer,
)
from digitalhub_runtime_container.entities.function.container.status import FunctionStatusContainer
from digitalhub_runtime_container.entities.function.container.utils import source_check

from digitalhub.entities.function._base.builder import FunctionBuilder


class FunctionContainerBuilder(FunctionBuilder, RuntimeEntityBuilderContainer):
    """
    FunctionContainer builder.
    """

    ENTITY_CLASS = FunctionContainer
    ENTITY_SPEC_CLASS = FunctionSpecContainer
    ENTITY_SPEC_VALIDATOR = FunctionValidatorContainer
    ENTITY_STATUS_CLASS = FunctionStatusContainer
    ENTITY_KIND = "container"

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
    ) -> FunctionContainer:
        kwargs = source_check(**kwargs)
        return super().build(
            kind,
            project,
            name,
            uuid,
            description,
            labels,
            embedded,
            **kwargs,
        )
