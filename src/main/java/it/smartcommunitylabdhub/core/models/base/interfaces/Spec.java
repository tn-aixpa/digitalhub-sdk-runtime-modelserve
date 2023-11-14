package it.smartcommunitylabdhub.core.models.base.interfaces;

import jakarta.validation.constraints.NotNull;

import java.util.Map;

/**
 * Base spec interface. Should be implemented by all specific Spec Ojbect.
 */
public interface Spec {
    void configure(@NotNull Map<String, Object> data);

    Map<String, Object> toMap();
}
