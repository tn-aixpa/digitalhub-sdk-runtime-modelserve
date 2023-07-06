package it.smartcommunitylabdhub.core.models.accessors.kinds.dataitems;

import java.util.LinkedHashMap;
import java.util.Map;

import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.DataItemFieldAccessor;

public class DatasetDataItemFieldAccessor implements DataItemFieldAccessor {

    private final Map<String, Object> fields;

    // private CommandFactory commandFactory;

    public DatasetDataItemFieldAccessor(Map<String, Object> fields) {
        this.fields = new LinkedHashMap<>(fields);
        // this.commandFactory = ConversionUtils.getCommandFactory();
    }

    @Override
    public Map<String, Object> getFields() {
        return this.fields;
    }

}
