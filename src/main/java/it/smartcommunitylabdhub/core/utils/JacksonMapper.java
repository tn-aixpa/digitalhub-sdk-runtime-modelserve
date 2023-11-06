package it.smartcommunitylabdhub.core.utils;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import it.smartcommunitylabdhub.core.models.base.specs.ConcreteSpecMixin;

import java.util.HashMap;

public class JacksonMapper {
    public static final ObjectMapper objectMapper = new ObjectMapper();
    public static final TypeReference<HashMap<String, Object>> typeRef =
            new TypeReference<>() {
            };

    static {
        // Configure the ObjectMapper to not fail on unknown properties
        objectMapper.configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false);
        objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        objectMapper.registerModule(new JavaTimeModule());
        objectMapper.addMixIn(BaseSpec.class, ConcreteSpecMixin.class); // Replace TaskTransformSpec with your concrete class
    }

    public static JavaType extractJavaType(Class<?> clazz) {
        // resolve generics type via subclass trick
        return objectMapper.getTypeFactory().constructSimpleType(clazz, null);
    }
}
