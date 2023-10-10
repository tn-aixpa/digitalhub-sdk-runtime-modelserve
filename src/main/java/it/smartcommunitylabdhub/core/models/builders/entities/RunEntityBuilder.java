package it.smartcommunitylabdhub.core.models.builders.entities;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.components.fsm.enums.RunState;
import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.run.Run;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;

@Component
public class RunEntityBuilder {

        /**
         * Build a Run from a RunDTO and store extra values as a cbor
         * 
         * @return
         */
        public Run build(RunDTO runDTO) {
                return EntityFactory.combine(
                                ConversionUtils.convert(runDTO, "run"), runDTO,
                                builder -> builder
                                                .with(r -> r.setMetadata(
                                                                ConversionUtils.convert(
                                                                                runDTO.getMetadata(),
                                                                                "metadata")))
                                                .with(r -> r.setExtra(
                                                                ConversionUtils.convert(
                                                                                runDTO.getExtra(),
                                                                                "cbor")))
                                                .with(r -> r.setSpec(
                                                                ConversionUtils.convert(
                                                                                runDTO.getSpec(),
                                                                                "cbor"))));

        }

        /**
         * Update a Run if element is not passed it override causing empty field
         * 
         * @param run
         * @return
         */
        public Run update(Run run, RunDTO runDTO) {
                return EntityFactory.combine(
                                run, runDTO, builder -> builder
                                                .with(r -> r.setKind(runDTO.getKind()))
                                                .with(r -> r.setTaskId(runDTO.getTaskId()))
                                                .with(r -> r.setProject(runDTO.getProject()))
                                                .with(r -> r.setTask(runDTO.getTask()))
                                                .with(r -> r.setState(runDTO.getState() == null
                                                                ? RunState.CREATED
                                                                : RunState.valueOf(
                                                                                runDTO.getState())))
                                                .with(r -> r.setMetadata(
                                                                ConversionUtils.convert(
                                                                                runDTO.getMetadata(),
                                                                                "metadata")))

                                                .with(r -> r.setExtra(
                                                                ConversionUtils.convert(
                                                                                runDTO.getExtra(),

                                                                                "cbor")))
                                                .with(r -> r.setSpec(
                                                                ConversionUtils.convert(
                                                                                runDTO.getSpec(),

                                                                                "cbor"))));
        }
}
