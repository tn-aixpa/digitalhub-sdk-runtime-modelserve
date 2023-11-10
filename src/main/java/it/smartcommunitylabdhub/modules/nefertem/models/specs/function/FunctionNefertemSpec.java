package it.smartcommunitylabdhub.modules.nefertem.models.specs.function;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.entities.function.specs.FunctionBaseSpec;
import lombok.Getter;
import lombok.Setter;


@Getter
@Setter
@SpecType(kind = "nefertem", entity = SpecEntity.FUNCTION)
public class FunctionNefertemSpec extends FunctionBaseSpec<FunctionNefertemSpec> {
    @Override
    protected void configureSpec(FunctionNefertemSpec functionNefertemSpec) {
    }
}
