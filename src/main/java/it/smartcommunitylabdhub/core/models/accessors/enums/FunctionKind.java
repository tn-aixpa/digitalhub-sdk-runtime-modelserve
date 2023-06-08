package it.smartcommunitylabdhub.core.models.accessors.enums;

import java.util.Map;

import it.smartcommunitylabdhub.core.models.accessors.kinds.functions.JobFunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.kinds.functions.NuclioFunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.kinds.functions.ServingFunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.FunctionFieldAccessor;

public enum FunctionKind {
    JOB("job", JobFunctionFieldAccessor::new),
    NUCLIO("nuclio", NuclioFunctionFieldAccessor::new),
    SERVING("serving", ServingFunctionFieldAccessor::new);

    private final String value;
    private final AccessorFactoryKind<FunctionFieldAccessor> accessorFactory;

    FunctionKind(String value, AccessorFactoryKind<FunctionFieldAccessor> accessorFactory) {
        this.value = value;
        this.accessorFactory = accessorFactory;
    }

    public String getValue() {
        return value;
    }

    public FunctionFieldAccessor createAccessor(Map<String, Object> fields) {
        return accessorFactory.create(fields);
    }
}