package it.smartcommunitylabdhub.core.models.converters.types;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.cbor.CBORFactory;
import it.smartcommunitylabdhub.core.annotations.common.ConverterType;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.base.metadata.BaseMetadata;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;

import java.io.IOException;

@ConverterType(type = "metadata")
public class MetadataConverter<M extends BaseMetadata>
        extends AbstractConverter implements Converter<M, byte[]> {

    @Override
    public byte[] convert(M metadata) throws CustomException {
        ObjectMapper objectMapper = new ObjectMapper(new CBORFactory());
        try {
            return objectMapper.writeValueAsBytes(metadata);
        } catch (JsonProcessingException e) {
            throw new CustomException(null, e);
        }
    }


    @Override
    public <C> C reverseByClass(byte[] cborBytes, Class<C> targetClass) throws CustomException {
        ObjectMapper objectMapper = new ObjectMapper(new CBORFactory());
        try {
            if (cborBytes == null) {
                return null;
            }
            return objectMapper.readValue(cborBytes, targetClass);
        } catch (IOException e) {
            throw new CustomException(null, e);
        }
    }

    @Override
    public M reverseConvert(byte[] cborBytes) throws CustomException {
        throw new UnsupportedOperationException("reverseConvert method not implemented." +
                "Call reverseByClass function instead passing the targetClass type.");
    }

}
