package it.smartcommunitylabdhub.core.models.accessors.kinds.functions;

import java.util.LinkedHashMap;
import java.util.Map;

import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.FunctionFieldAccessor;

public class JobFunctionFieldAccessor implements FunctionFieldAccessor {

    private final Map<String, Object> fields;

    // private CommandFactory commandFactory;

    public JobFunctionFieldAccessor(Map<String, Object> fields) {
        this.fields = new LinkedHashMap<>(fields);
    }

    @Override
    public Map<String, Object> getFields() {
        return this.fields;
    }

    // get code origin
    public String getCodeOrigin() {
        return mapHasField(getBuild(), "code_origin") ? (String) getBuild().get("code_origin") : null;
    }

    public String getOriginFilename() {
        return mapHasField(getBuild(), "origin_filename") ? (String) getBuild().get("origin_filename") : null;
    }

}
