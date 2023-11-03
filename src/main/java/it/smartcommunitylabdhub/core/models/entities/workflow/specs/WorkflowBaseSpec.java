package it.smartcommunitylabdhub.core.models.entities.workflow.specs;

import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class WorkflowBaseSpec<S extends WorkflowBaseSpec<S>> extends BaseSpec<S> {
    @Override
    protected void configureSpec(S concreteSpec) {

    }
}
