package it.smartcommunitylabdhub.core.models.converters.types;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.dtos.LogDTO;
import it.smartcommunitylabdhub.core.models.entities.Log;

@Component
public class LogConverter implements Converter<LogDTO, Log> {

    @Override
    public Log convert(LogDTO logDTO) throws CustomException {
        return Log.builder()
                .id(logDTO.getId())
                .project(logDTO.getProject())
                .run(logDTO.getRun())
                .body(ConversionUtils.convert(logDTO.getBody(), "cbor"))
                .build();
    }

    @Override
    public LogDTO reverseConvert(Log log) throws CustomException {
        return LogDTO.builder()
                .id(log.getId())
                .project(log.getProject())
                .run(log.getRun())
                .body(ConversionUtils.reverse(log.getBody(), "cbor"))
                .created(log.getCreated())
                .updated(log.getUpdated())
                .build();
    }

}