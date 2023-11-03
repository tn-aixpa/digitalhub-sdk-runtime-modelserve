package it.smartcommunitylabdhub.core.models.base.specs;

import com.fasterxml.jackson.annotation.JsonAnySetter;

public abstract class ConcreteSpecMixin {
    @JsonAnySetter
    public abstract void handleUnknownProperties(String key, Object value);
}