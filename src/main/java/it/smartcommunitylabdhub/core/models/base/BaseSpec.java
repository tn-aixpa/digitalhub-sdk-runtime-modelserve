package it.smartcommunitylabdhub.core.models.base;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import lombok.Getter;
import lombok.Setter;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

@Getter
@Setter
public class BaseSpec implements Spec {
    private Map<String, Object> extra = new HashMap<>();

    @JsonAnyGetter
    public Map<String, Object> getExtra() {
        return extra;
    }

    @JsonAnySetter
    public void setExtra(String key, Object value) {
        this.extra.put(key, value);
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
                    extra.put(fieldName, value);
                }
            } catch (IllegalAccessException e) {
                // Handle IllegalAccessException
            }
        }
    }

    @Override
    public Map<String, Object> toMap() {
        Map<String, Object> result = new HashMap<>();

        // Serialize all fields (including extraSpecs) to a JSON map
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            String json = objectMapper.writeValueAsString(this);

            // Convert the JSON string to a map
            Map<String, Object> serializedMap = objectMapper.readValue(json, new TypeReference<>() {
            });

            // Include extra properties in the result map
            result.putAll(serializedMap);
            result.putAll(extra);

            return result;
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Error converting to Map", e);
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
