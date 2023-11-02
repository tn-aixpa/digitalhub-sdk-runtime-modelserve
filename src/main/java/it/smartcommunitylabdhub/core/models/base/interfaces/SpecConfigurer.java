package it.smartcommunitylabdhub.core.models.base.interfaces;

import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;

public interface SpecConfigurer {
    <S extends T, T extends BaseSpec> void configure(S concreteSpec);
}
