package it.smartcommunitylabdhub.core.models.base.specs;


import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "none", entity = SpecEntity.NONE)
public class NoneBaseSpec<S extends NoneBaseSpec> extends BaseSpec<S> {
    @Override
    protected void configureSpec(S concreteSpec) {
    }
}
