package it.smartcommunitylabdhub.core.models.converters.types;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.entities.function.Function;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class FunctionConverter implements Converter<FunctionDTO, Function> {

    @Override
    public Function convert(FunctionDTO functionDTO) throws CustomException {
        return Function.builder()
                .id(functionDTO.getId())
                .name(functionDTO.getName())
                .kind(functionDTO.getKind())
                .project(functionDTO.getProject())
                .embedded(functionDTO.getEmbedded())
                .state(functionDTO.getState() == null ? State.CREATED
                        : State.valueOf(functionDTO.getState()))
                .build();
    }

    @Override
    public FunctionDTO reverseConvert(Function function) throws CustomException {
        return FunctionDTO.builder()
                .id(function.getId())
                .name(function.getName())
                .kind(function.getKind())
                .project(function.getProject())
                .embedded(function.getEmbedded())
                .state(function.getState() == null ? State.CREATED.name()
                        : function.getState().name())
                .created(function.getCreated())
                .updated(function.getUpdated())
                .build();
    }

}
