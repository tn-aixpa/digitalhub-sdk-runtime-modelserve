package it.smartcommunitylabdhub.core.models.accessors.enums;

import java.lang.reflect.Method;
import java.util.Map;

import it.smartcommunitylabdhub.core.models.accessors.kinds.dataitems.DatasetDataItemFieldAccessor;
import it.smartcommunitylabdhub.core.models.accessors.kinds.interfaces.DataItemFieldAccessor;

public enum DataItemKind {

    DATASET("dataset", DatasetDataItemFieldAccessor::new, DatasetDataItemFieldAccessor.class);

    private final String value;
    private final AccessorFactoryKind<DataItemFieldAccessor> accessorFactory;
    private final Class<? extends DataItemFieldAccessor> accessorClass;

    DataItemKind(String value, AccessorFactoryKind<DataItemFieldAccessor> accessorFactory,
            Class<? extends DataItemFieldAccessor> accessorClass) {
        this.value = value;
        this.accessorFactory = accessorFactory;
        this.accessorClass = accessorClass;
    }

    public String getValue() {
        return value;
    }

    public DataItemFieldAccessor createAccessor(Map<String, Object> fields) {
        return accessorFactory.create(fields);
    }

    @SuppressWarnings("unchecked")
    public <T> T invokeMethod(DataItemFieldAccessor accessor, String methodName) {
        if (accessorClass != null) {
            try {
                Method method = accessorClass.getMethod(methodName);
                return (T) method.invoke(accessor);
            } catch (Exception e) {
                // Handle any exceptions that occur during method invocation
                e.printStackTrace();
            }
        }
        return null;
    }
}
