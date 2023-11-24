package it.smartcommunitylabdhub.core.models.converters.types;

import it.smartcommunitylabdhub.core.annotations.common.ConverterType;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionEntity;
import it.smartcommunitylabdhub.core.models.entities.function.Function;
import it.smartcommunitylabdhub.core.models.enums.State;

@ConverterType(type = "function")
public class FunctionConverter implements Converter<Function, FunctionEntity> {

        @Override
        public FunctionEntity convert(Function functionDTO) throws CustomException {
                return FunctionEntity.builder()
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
        public Function reverseConvert(FunctionEntity function) throws CustomException {
                return Function.builder()
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
