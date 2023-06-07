package it.smartcommunitylabdhub.core.models.accessors.functions;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylabdhub.core.models.accessors.interfaces.FunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.converters.CommandFactory;

public class JobFunctionFieldAccessor implements FunctionFieldAccessor {

    private final Map<String, Object> fields;

    @Autowired
    private CommandFactory commandFactory;

    public JobFunctionFieldAccessor(Map<String, Object> fields) {
        this.fields = Collections.unmodifiableMap(new LinkedHashMap<>(fields));
    }

    @Override
    public Map<String, Object> getFields() {
        return this.fields;
    }

    //
}
