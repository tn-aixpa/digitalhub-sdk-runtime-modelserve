package it.smartcommunitylabdhub.core.models.accessors.enums;

import java.util.Map;

import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.ProjectFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.kinds.projects.MlrunProjectFieldAccessor;

public enum ProjectKind {
    MLRUN("mlrun", MlrunProjectFieldAccessor::new);

    private final String value;
    private final AccessorFactoryKind<ProjectFieldAccessor> accessorFactory;

    ProjectKind(String value, AccessorFactoryKind<ProjectFieldAccessor> accessorFactory) {
        this.value = value;
        this.accessorFactory = accessorFactory;
    }

    public String getValue() {
        return value;
    }

    public ProjectFieldAccessor createAccessor(Map<String, Object> fields) {
        return accessorFactory.create(fields);
    }
}
