package it.smartcommunitylabdhub.core.models.base;

import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;

public class JacksonMapper {
    protected static final ObjectMapper mapper = new ObjectMapper();

    protected JavaType _extractJavaType(Class<?> clazz) {
        // resolve generics type via subclass trick
        return mapper.getTypeFactory().constructSimpleType(clazz, null);
    }
}
