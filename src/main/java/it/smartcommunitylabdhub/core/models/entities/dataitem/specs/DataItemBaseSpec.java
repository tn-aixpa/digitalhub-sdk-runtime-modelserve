package it.smartcommunitylabdhub.core.models.entities.dataitem.specs;

import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import lombok.Getter;
import lombok.Setter;


@Getter
@Setter
public class DataItemBaseSpec<S extends DataItemBaseSpec<S>> extends BaseSpec<S> {
    private String key;
    private String path;

    @Override
    protected void configureSpec(S concreteSpec) {
    }
}
