package it.smartcommunitylabdhub.core.models.builders.entities;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.Function;
import it.smartcommunitylabdhub.core.models.enums.State;

public class FunctionEntityBuilder {

        private FunctionDTO functionDTO;

        public FunctionEntityBuilder(
                        FunctionDTO functionDTO) {
                this.functionDTO = functionDTO;
        }

        /**
         * Build a function from a functionDTO and store extra values as a cbor
         * 
         * @return
         */
        public Function build() {
                Function function = EntityFactory.combine(
                                ConversionUtils.convert(functionDTO, "function"), functionDTO,
                                builder -> {
                                        builder
                                                        .with(f -> f.setExtra(
                                                                        ConversionUtils.convert(functionDTO.getExtra(),
                                                                                        "cbor")))
                                                        .with(f -> f.setSpec(
                                                                        ConversionUtils.convert(functionDTO.getSpec(),
                                                                                        "cbor")));
                                });

                return function;
        }

        /**
         * Update a function
         * TODO: x because if element is not passed it override causing empty field
         * 
         * @param function
         * @return
         */
        public Function update(Function function) {
                return EntityFactory.combine(
                                function, functionDTO, builder -> {
                                        builder
                                                        .with(f -> f.setKind(functionDTO.getKind()))
                                                        .with(f -> f.setProject(functionDTO.getProject()))
                                                        .with(f -> f.setState(functionDTO.getState() == null
                                                                        ? State.CREATED
                                                                        : State.valueOf(functionDTO.getState())))
                                                        .with(f -> f.setExtra(
                                                                        ConversionUtils.convert(functionDTO.getExtra(),

                                                                                        "cbor")))
                                                        .with(f -> f.setSpec(
                                                                        ConversionUtils.convert(functionDTO.getSpec(),

                                                                                        "cbor")))
                                                        .with(f -> f.setEmbedded(functionDTO.getEmbedded()));
                                });
        }
}