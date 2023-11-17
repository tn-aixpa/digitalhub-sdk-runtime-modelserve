package it.smartcommunitylabdhub.core.models.accessors.enums;

import it.smartcommunitylabdhub.core.models.accessors.kinds.functions.JobFunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.kinds.functions.NuclioFunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.kinds.functions.ServingFunctionFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.FunctionFieldAccessor;
import lombok.extern.slf4j.Slf4j;

import java.lang.reflect.Method;
import java.util.Map;

@Slf4j
public enum FunctionKind {
    JOB("job", JobFunctionFieldAccessor::new, JobFunctionFieldAccessor.class),
    /**
     *
     */
    NUCLIO("nuclio", NuclioFunctionFieldAccessor::new, NuclioFunctionFieldAccessor.class),
    /**
     *
     */
    SERVING("serving", ServingFunctionFieldAccessor::new, ServingFunctionFieldAccessor.class);

    private final String value;
    private final AccessorFactoryKind<FunctionFieldAccessor> accessorFactory;
    private final Class<? extends FunctionFieldAccessor> accessorClass;

    FunctionKind(String value, AccessorFactoryKind<FunctionFieldAccessor> accessorFactory,
                 Class<? extends FunctionFieldAccessor> accessorClass) {
        this.value = value;
        this.accessorFactory = accessorFactory;
        this.accessorClass = accessorClass;
    }

    public String getValue() {
        return value;
    }

    public FunctionFieldAccessor createAccessor(Map<String, Object> fields) {
        return accessorFactory.create(fields);
    }

    @SuppressWarnings("unchecked")
    public <T> T invokeMethod(FunctionFieldAccessor accessor, String methodName) {
        if (accessorClass != null) {
            try {
                Method method = accessorClass.getMethod(methodName);
                return (T) method.invoke(accessor);
            } catch (Exception e) {
                // Handle any exceptions that occur during method invocation
                log.error(e.getMessage());
            }
        }
        return null;
    }
}
