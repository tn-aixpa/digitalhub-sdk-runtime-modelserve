package it.smartcommunitylabdhub.core.models.base.interfaces;

import java.util.Map;

/**
 * Base spec interface. Should be implemented by all specific Spec Ojbect.
 */
public interface Spec {
    void configure(Map<String, Object> data);

    Map<String, Object> toMap();
}
