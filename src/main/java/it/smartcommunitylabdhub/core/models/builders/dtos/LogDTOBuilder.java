package it.smartcommunitylabdhub.core.models.builders.dtos;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.LogDTO;
import it.smartcommunitylabdhub.core.models.entities.Log;
import it.smartcommunitylabdhub.core.models.enums.State;

public class LogDTOBuilder {

        private Log log;

        public LogDTOBuilder(
                        Log log) {
                this.log = log;
        }

        public LogDTO build() {
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