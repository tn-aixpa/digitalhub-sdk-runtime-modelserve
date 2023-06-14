package it.smartcommunitylabdhub.core.models.accessors.kinds.projects;

import java.util.LinkedHashMap;
import java.util.Map;

import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.ProjectFieldAccessor;

public class MlrunProjectFieldAccessor implements ProjectFieldAccessor {

    private final Map<String, Object> fields;

    public MlrunProjectFieldAccessor(Map<String, Object> fields) {
        this.fields = new LinkedHashMap<>(fields);
    }

    @Override
    public Map<String, Object> getFields() {
        return this.fields;
    }

    //
}
