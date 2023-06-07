package it.smartcommunitylabdhub.core.models.accessors.enums.kinds;

import java.util.Map;

import it.smartcommunitylabdhub.core.models.accessors.functions.JobFunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.functions.NuclioFunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.functions.ServingFunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.interfaces.FunctionFieldAccessor;

public enum FunctionKind {
    JOB("job", JobFunctionFieldAccessor::new),
    NUCLIO("nuclio", NuclioFunctionFieldAccessor::new),
    SERVING("serving", ServingFunctionFieldAccessor::new);

    private final String value;
    private final FunctionAccessorFactory accessorFactory;

    FunctionKind(String value, FunctionAccessorFactory accessorFactory) {
        this.value = value;
        this.accessorFactory = accessorFactory;
    }

    public String getValue() {
        return value;
    }

    public FunctionFieldAccessor createAccessor(Map<String, Object> fields) {
        return accessorFactory.create(fields);
    }

    @FunctionalInterface
    private interface FunctionAccessorFactory {
        FunctionFieldAccessor create(Map<String, Object> fields);
    }
}