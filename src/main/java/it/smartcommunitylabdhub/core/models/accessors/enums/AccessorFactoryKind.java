package it.smartcommunitylabdhub.core.models.accessors.enums.kinds;

import java.util.Map;

@FunctionalInterface
public interface AccessorFactoryKind<T> {
    T create(Map<String, Object> fields);
}