package it.smartcommunitylabdhub.core.models.builders.entities;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.Run;
import it.smartcommunitylabdhub.core.models.enums.State;

public class RunEntityBuilder {

        private RunDTO runDTO;

        public RunEntityBuilder(
                        RunDTO runDTO) {
                this.runDTO = runDTO;
        }

        /**
         * Build a Run from a RunDTO and store extra values as a cbor
         * 
         * @return
         */
        public Run build() {
                Run Run = EntityFactory.combine(
                                ConversionUtils.convert(runDTO, "run"), runDTO,
                                builder -> {
                                        builder
                                                        .with(f -> f.setExtra(
                                                                        ConversionUtils.convert(runDTO.getExtra(),
                                                                                        "cbor")))
                                                        .with(f -> f.setBody(
                                                                        ConversionUtils.convert(runDTO.getBody(),
                                                                                        "cbor")));
                                });

                return Run;
        }

        /**
         * Update a Run
         * TODO: x because if element is not passed it override causing empty field
         * 
         * @param Run
         * @return
         */
        public Run update(Run Run) {
                return EntityFactory.combine(
                                Run, runDTO, builder -> {
                                        builder
                                                        .with(f -> f.setType(runDTO.getType()))
                                                        .with(f -> f.setProject(runDTO.getProject()))
                                                        .with(f -> f.setName(runDTO.getName()))
                                                        .with(f -> f.setState(runDTO.getState() == null
                                                                        ? State.CREATED
                                                                        : State.valueOf(runDTO.getState())))
                                                        .with(f -> f.setExtra(
                                                                        ConversionUtils.convert(runDTO.getExtra(),

                                                                                        "cbor")))
                                                        .with(f -> f.setBody(
                                                                        ConversionUtils.convert(runDTO.getBody(),

                                                                                        "cbor")));
                                });
        }
}