from __future__ import annotations

from digitalhub_runtime_dbt.entities._base.runtime_entity.builder import RuntimeEntityBuilderDbt
from digitalhub_runtime_dbt.entities.function.dbt.entity import FunctionDbt
from digitalhub_runtime_dbt.entities.function.dbt.spec import FunctionSpecDbt, FunctionValidatorDbt
from digitalhub_runtime_dbt.entities.function.dbt.status import FunctionStatusDbt
from digitalhub_runtime_dbt.entities.function.dbt.utils import source_check, source_post_check

from digitalhub.entities.function._base.builder import FunctionBuilder


class FunctionDbtBuilder(FunctionBuilder, RuntimeEntityBuilderDbt):
    """
    FunctionDbt builder.
    """

    ENTITY_CLASS = FunctionDbt
    ENTITY_SPEC_CLASS = FunctionSpecDbt
    ENTITY_SPEC_VALIDATOR = FunctionValidatorDbt
    ENTITY_STATUS_CLASS = FunctionStatusDbt
    ENTITY_KIND = "dbt"

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
    ) -> FunctionDbt:
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
