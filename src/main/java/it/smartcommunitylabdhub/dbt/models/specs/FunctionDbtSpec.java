package it.smartcommunitylabdhub.dbt.models.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import it.smartcommunitylabdhub.core.models.entities.function.specs.FunctionBaseSpec;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@SpecType(kind = "dbt", entity = SpecEntity.FUNCTION)
public class FunctionDbtSpec extends FunctionBaseSpec {
    private String image;
    private String command;
    private List<String> args;
    private String sql;

    @Override
    protected <S extends T, T extends BaseSpec> void configure(S concreteSpec) {
        FunctionDbtSpec functionDbtSpec = (FunctionDbtSpec) concreteSpec;
        this.setSource(functionDbtSpec.getSource());
        this.setImage(functionDbtSpec.getImage());
        this.setArgs(functionDbtSpec.getArgs());
        this.setSql(functionDbtSpec.getSql());
        this.setCommand(functionDbtSpec.getCommand());
        this.setExtraSpecs(functionDbtSpec.getExtraSpecs());
    }
}
