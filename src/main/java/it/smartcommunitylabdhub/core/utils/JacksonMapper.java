package it.smartcommunitylabdhub.core.utils;

import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;

public class JacksonMapper {
    public static final ObjectMapper objectMapper = new ObjectMapper();

    public static JavaType _extractJavaType(Class<?> clazz) {
        // resolve generics type via subclass trick
        return objectMapper.getTypeFactory().constructSimpleType(clazz, null);
    }
}
