package it.smartcommunitylabdhub.core.models.accessors.enums;

import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.ProjectFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.kinds.projects.MlrunProjectFieldAccessor;
import lombok.extern.slf4j.Slf4j;

import java.lang.reflect.Method;
import java.util.Map;

@Slf4j
public enum ProjectKind {
    MLRUN("mlrun", MlrunProjectFieldAccessor::new, MlrunProjectFieldAccessor.class);

    private final String value;
    private final AccessorFactoryKind<ProjectFieldAccessor> accessorFactory;
    private final Class<? extends ProjectFieldAccessor> accessorClass;

    ProjectKind(String value, AccessorFactoryKind<ProjectFieldAccessor> accessorFactory,
                Class<? extends ProjectFieldAccessor> accessorClass) {
        this.value = value;
        this.accessorFactory = accessorFactory;
        this.accessorClass = accessorClass;
    }

    public String getValue() {
        return value;
    }

    public ProjectFieldAccessor createAccessor(Map<String, Object> fields) {
        return accessorFactory.create(fields);
    }

    @SuppressWarnings("unchecked")
    public <T> T invokeMethod(ProjectFieldAccessor accessor, String methodName) {
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
