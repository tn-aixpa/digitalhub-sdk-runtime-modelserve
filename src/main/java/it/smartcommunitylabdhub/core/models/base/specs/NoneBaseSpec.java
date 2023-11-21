package it.smartcommunitylabdhub.core.models.base.specs;


import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class NoneBaseSpec<S extends NoneBaseSpec<S>> extends BaseSpec<S> {

    @Override
    protected void configureSpec(S concreteSpec) {

    }
}
