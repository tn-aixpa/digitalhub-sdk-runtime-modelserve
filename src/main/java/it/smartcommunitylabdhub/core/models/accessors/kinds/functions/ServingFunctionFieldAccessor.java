package it.smartcommunitylabdhub.core.models.accessors.kinds.functions;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.FunctionFieldAccessor;

public class ServingFunctionFieldAccessor implements FunctionFieldAccessor {

    private final Map<String, Object> fields;

    public ServingFunctionFieldAccessor(Map<String, Object> fields) {
        this.fields = Collections.unmodifiableMap(new LinkedHashMap<>(fields));

    }

    @Override
    public Map<String, Object> getFields() {
        return this.fields;
    }

}
