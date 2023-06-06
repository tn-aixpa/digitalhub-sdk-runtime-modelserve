package it.smartcommunitylabdhub.core.services.builders.entities;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.Function;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.services.factory.EntityFactory;

public class FunctionEntityBuilder {

        private CommandFactory commandFactory;
        private FunctionDTO functionDTO;

        public FunctionEntityBuilder(
                        CommandFactory commandFactory,
                        FunctionDTO functionDTO) {
                this.functionDTO = functionDTO;
                this.commandFactory = commandFactory;
        }

        /**
         * Build a function from a functionDTO and store extra values as a cbor
         * 
         * @return
         */
        public Function build() {
                Function function = EntityFactory.combine(
                                ConversionUtils.convert(functionDTO, commandFactory, "function"), functionDTO,
                                builder -> {
                                        builder
                                                        .with(f -> f.setExtra(
                                                                        ConversionUtils.convert(functionDTO.getExtra(),
                                                                                        commandFactory,
                                                                                        "cbor")))
                                                        .with(f -> f.setSpec(
                                                                        ConversionUtils.convert(functionDTO.getSpec(),
                                                                                        commandFactory,
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
                                                                                        commandFactory,
                                                                                        "cbor")))
                                                        .with(f -> f.setSpec(
                                                                        ConversionUtils.convert(functionDTO.getSpec(),
                                                                                        commandFactory,
                                                                                        "cbor")))
                                                        .with(f -> f.setEmbedded(functionDTO.getEmbedded()));
                                });
        }
}