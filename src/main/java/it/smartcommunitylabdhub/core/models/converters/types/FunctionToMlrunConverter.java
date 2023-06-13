package it.smartcommunitylabdhub.core.models.converters.types;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;

public class FunctionToMlrunConverter implements Converter<FunctionDTO, Map<String, Object>> {

    @Override
    public Map<String, Object> convert(FunctionDTO functionDTO) throws CustomException {
        Map<String, Object> mlrunFunction = new HashMap<>();
        Map<String, Object> metadata = new HashMap<>();

        metadata.put("name", functionDTO.getName());
        metadata.put("project", functionDTO.getProject());
        metadata.put("tag", Optional.ofNullable(functionDTO.getExtra().get("tag")).orElse(""));
        metadata.put("categories",
                Optional.ofNullable(functionDTO.getExtra().get("categories")).orElse(new ArrayList<>()));

        mlrunFunction.put("metadata", metadata);
        mlrunFunction.put("kind", functionDTO.getKind());
        mlrunFunction.put("spec", functionDTO.getSpec());

        return mlrunFunction;
    }

    @Override
    public FunctionDTO reverseConvert(Map<String, Object> input) throws CustomException {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'reverseConvert'");
    }

}