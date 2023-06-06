package it.smartcommunitylabdhub.core.services.builders.dtos;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.Function;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.services.factory.EntityFactory;

public class FunctionDTOBuilder {

        private CommandFactory commandFactory;
        private Function function;

        public FunctionDTOBuilder(
                        CommandFactory commandFactory,
                        Function function) {
                this.function = function;
                this.commandFactory = commandFactory;
        }

        public FunctionDTO build() {
                return EntityFactory.create(FunctionDTO::new, function, builder -> {
                        builder
                                        .with(dto -> dto.setId(function.getId()))
                                        .with(dto -> dto.setKind(function.getKind()))
                                        .with(dto -> dto.setProject(function.getProject()))
                                        .with(dto -> dto.setName(function.getName()))
                                        .with(dto -> dto.setSpec(ConversionUtils.reverse(
                                                        function.getSpec(),
                                                        commandFactory,
                                                        "cbor")))
                                        .with(dto -> dto.setExtra(ConversionUtils.reverse(
                                                        function.getExtra(),
                                                        commandFactory,
                                                        "cbor")))
                                        .with(dto -> dto.setState(function.getState() == null ? State.CREATED.name()
                                                        : function.getState().name()))
                                        .with(dto -> dto.setCreated(function.getCreated()))
                                        .with(dto -> dto.setUpdated(function.getUpdated()))
                                        .with(dto -> dto.setEmbedded(function.getEmbedded()))
                                        .with(dto -> dto.setState(function.getState() == null ? State.CREATED.name()
                                                        : function.getState().name()));

                });
        }
}