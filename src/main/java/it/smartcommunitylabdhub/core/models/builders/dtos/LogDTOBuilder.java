package it.smartcommunitylabdhub.core.models.builders.dtos;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.LogDTO;
import it.smartcommunitylabdhub.core.models.entities.Log;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class LogDTOBuilder {

        public LogDTO build(Log log) {
                return EntityFactory.create(LogDTO::new, log, builder -> {
                        builder
                                        .with(dto -> dto.setId(log.getId()))
                                        .with(dto -> dto.setRun(log.getRun()))
                                        .with(dto -> dto.setProject(log.getProject()))
                                        .with(dto -> dto.setBody(ConversionUtils.reverse(log.getBody(), "cbor")))
                                        .with(dto -> dto.setExtra(ConversionUtils.reverse(log.getExtra(), "cbor")))
                                        .with(dto -> dto.setCreated(log.getCreated()))
                                        .with(dto -> dto.setUpdated(log.getUpdated()))
                                        .with(dto -> dto.setState(log.getState() == null
                                                        ? State.CREATED.name()
                                                        : log.getState()
                                                                        .name()));

                });
        }
}