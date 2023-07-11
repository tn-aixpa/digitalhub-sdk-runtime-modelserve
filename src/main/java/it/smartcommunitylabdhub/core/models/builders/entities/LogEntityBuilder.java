package it.smartcommunitylabdhub.core.models.builders.entities;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.LogDTO;
import it.smartcommunitylabdhub.core.models.entities.Log;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class LogEntityBuilder {

        /**
         * Build a Log from a LogDTO and store extra values as a cbor
         * 
         * @return
         */
        public Log build(LogDTO logDTO) {
                Log Log = EntityFactory.combine(
                                ConversionUtils.convert(logDTO, "log"), logDTO,
                                builder -> {
                                        builder
                                                        .with(f -> f.setExtra(
                                                                        ConversionUtils.convert(logDTO.getExtra(),
                                                                                        "cbor")))
                                                        .with(f -> f.setBody(
                                                                        ConversionUtils.convert(logDTO.getBody(),
                                                                                        "cbor")));
                                });

                return Log;
        }

        /**
         * Update a Log
         * if element is not passed it override causing empty field
         * 
         * @param Log
         * @return
         */
        public Log update(Log Log, LogDTO logDTO) {
                return EntityFactory.combine(
                                Log, logDTO, builder -> {
                                        builder
                                                        .with(f -> f.setRun(logDTO.getRun()))
                                                        .with(f -> f.setProject(logDTO.getProject()))
                                                        .with(f -> f.setState(logDTO.getState() == null
                                                                        ? State.CREATED
                                                                        : State.valueOf(logDTO.getState())))
                                                        .with(f -> f.setExtra(
                                                                        ConversionUtils.convert(logDTO.getExtra(),

                                                                                        "cbor")))
                                                        .with(f -> f.setBody(
                                                                        ConversionUtils.convert(logDTO.getBody(),

                                                                                        "cbor")));
                                });
        }
}