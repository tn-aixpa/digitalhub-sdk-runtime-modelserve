package it.smartcommunitylabdhub.core.models.converters.types;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.cbor.CBORFactory;
import it.smartcommunitylabdhub.core.annotations.common.ConverterType;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@ConverterType(type = "cbor")
public class CBORConverter implements Converter<Map<String, Object>, byte[]> {

    @Override
    public byte[] convert(Map<String, Object> map) throws CustomException {
        ObjectMapper objectMapper = new ObjectMapper(new CBORFactory());
        try {
            return objectMapper.writeValueAsBytes(map);
        } catch (JsonProcessingException e) {
            throw new CustomException(null, e);
        }
    }

    @Override
    public Map<String, Object> reverseConvert(byte[] cborBytes) throws CustomException {
        ObjectMapper objectMapper = new ObjectMapper(new CBORFactory());
        try {
            if (cborBytes == null) {
                return new HashMap<>();
            }
            return objectMapper.readValue(cborBytes, new TypeReference<Map<String, Object>>() {});
        } catch (IOException e) {
            throw new CustomException(null, e);
        }
    }
}
