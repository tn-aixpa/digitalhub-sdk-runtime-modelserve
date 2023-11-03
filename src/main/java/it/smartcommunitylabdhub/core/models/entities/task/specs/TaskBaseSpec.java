package it.smartcommunitylabdhub.core.models.entities.task.specs;

import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class TaskBaseSpec<S extends TaskBaseSpec<S>> extends BaseSpec<S> {
    String function;

    @Override
    protected void configureSpec(S concreteSpec) {
        this.setFunction(concreteSpec.getFunction());
        this.setExtraSpecs(concreteSpec.getExtraSpecs());
    }
}
