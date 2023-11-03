package it.smartcommunitylabdhub.core.models.base.interfaces;

import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;

import java.util.Map;

/**
 * Base spec interface. Should be implemented by all specific Spec Ojbect.
 */
public interface Spec<S extends BaseSpec<S>> {
    void configure(Map<String, Object> data);

    Map<String, Object> toMap();
}
