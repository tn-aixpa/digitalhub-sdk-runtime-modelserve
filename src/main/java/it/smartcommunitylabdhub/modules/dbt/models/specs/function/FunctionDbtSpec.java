package it.smartcommunitylabdhub.modules.dbt.models.specs.function;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.entities.function.specs.FunctionBaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "dbt", entity = SpecEntity.FUNCTION)
public class FunctionDbtSpec extends FunctionBaseSpec<FunctionDbtSpec> {
    private String sql;

    @Override
    protected void configureSpec(FunctionDbtSpec functionDbtSpec) {
        super.configureSpec(functionDbtSpec);

        this.setSql(functionDbtSpec.getSql());
    }
}
