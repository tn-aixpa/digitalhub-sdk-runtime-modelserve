package it.smartcommunitylabdhub.core.models.converters.types;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.dtos.LogDTO;
import it.smartcommunitylabdhub.core.models.entities.Log;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class LogConverter implements Converter<LogDTO, Log> {

    @Override
    public Log convert(LogDTO logDTO) throws CustomException {
        return Log.builder()
                .id(logDTO.getId())
                .project(logDTO.getProject())
                .run(logDTO.getRun())
                .state(logDTO.getState() == null ? State.CREATED : State.valueOf(logDTO.getState()))
                .build();
    }

    @Override
    public LogDTO reverseConvert(Log log) throws CustomException {
        return LogDTO.builder()
                .id(log.getId())
                .project(log.getProject())
                .run(log.getRun())
                .state(log.getState() == null ? State.CREATED.name() : log.getState().name())
                .created(log.getCreated())
                .updated(log.getUpdated())
                .build();
    }

}