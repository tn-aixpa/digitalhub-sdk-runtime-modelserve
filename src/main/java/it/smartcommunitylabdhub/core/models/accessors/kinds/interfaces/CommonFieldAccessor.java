package it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces;

import java.util.Map;

public interface CommonFieldAccessor extends FieldAccessor<Object> {

    default String getKind() {
        return (String) getField("kind");
    }

    @SuppressWarnings("unchecked")
    default Map<String, Object> getMetadata() {
        return (Map<String, Object>) getField("metadata");
    }

    @SuppressWarnings("unchecked")
    default Map<String, Object> getSpecs() {
        return (Map<String, Object>) getField("spec");
    }

    @SuppressWarnings("unchecked")
    default Map<String, Object> getStatus() {
        return (Map<String, Object>) getField("status");
    }

    default boolean getVerbose() {
        return (boolean) getField("verbose");
    }

}
