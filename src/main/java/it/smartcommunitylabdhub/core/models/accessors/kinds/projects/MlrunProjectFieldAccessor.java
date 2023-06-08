package it.smartcommunitylabdhub.core.models.accessors.projects;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;

import it.smartcommunitylabdhub.core.models.accessors.interfaces.ProjectFieldAccessor;
import it.smartcommunitylabdhub.core.models.converters.CommandFactory;

public class MlrunProjectFieldAccessor implements ProjectFieldAccessor {

    private final Map<String, Object> fields;

    @Autowired
    private CommandFactory commandFactory;

    public MlrunProjectFieldAccessor(Map<String, Object> fields) {
        this.fields = Collections.unmodifiableMap(new LinkedHashMap<>(fields));
    }

    @Override
    public Map<String, Object> getFields() {
        return this.fields;
    }

    //
}
