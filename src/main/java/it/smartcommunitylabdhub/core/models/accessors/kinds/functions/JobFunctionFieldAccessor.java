package it.smartcommunitylabdhub.core.models.accessors.kinds.functions;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Configurable;

import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.FunctionFieldAccessor;

@Configurable
public class JobFunctionFieldAccessor implements FunctionFieldAccessor {

    private final Map<String, Object> fields;

    // private CommandFactory commandFactory;

    public JobFunctionFieldAccessor(Map<String, Object> fields) {
        this.fields = Collections.unmodifiableMap(new LinkedHashMap<>(fields));
        // this.commandFactory = ConversionUtils.getCommandFactory();
    }

    @Override
    public Map<String, Object> getFields() {
        return this.fields;
    }

    //
}
