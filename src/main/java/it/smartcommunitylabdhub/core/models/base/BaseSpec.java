package it.smartcommunitylabdhub.core.models.base;

import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import lombok.Getter;
import lombok.Setter;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

@Getter
@Setter
public class BaseSpec implements Spec {
    private Map<String, Object> extraSpecs = new HashMap<>();

    public void setExtraSpec(String key, Object value) {
        this.getExtraSpecs().put(key, value);
    }

    @SuppressWarnings("unchecked")
    public <T> T getExtraSpec(String key) {
        return (T) extraSpecs.get(key);
    }

    @Override
    public void configure(Map<String, Object> data) {
        for (Map.Entry<String, Object> entry : data.entrySet()) {
            String fieldName = entry.getKey();
            Object value = entry.getValue();

            Field field;
            try {
                field = findFieldInHierarchy(this.getClass(), fieldName);
                if (field != null) {
                    field.setAccessible(true);
                    field.set(this, value);
                } else {
                    // Field not found in the hierarchy, store in extraSpec map
                    extraSpecs.put(fieldName, value);
                }
            } catch (IllegalAccessException e) {
                // Handle IllegalAccessException
            }
        }
    }

    private Field findFieldInHierarchy(Class<?> clazz, String fieldName) {
        while (clazz != null) {
            try {
                return clazz.getDeclaredField(fieldName);
            } catch (NoSuchFieldException e) {
                // Field not found in this class, try the superclass
                clazz = clazz.getSuperclass();
            }
        }
        return null; // Field not found in the hierarchy
    }

}
