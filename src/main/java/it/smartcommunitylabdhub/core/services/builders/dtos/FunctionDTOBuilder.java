package it.smartcommunitylabdhub.core.services.builders.dtos;

import java.util.Optional;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.Function;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.services.factory.EntityFactory;

public class FunctionDTOBuilder {

        private CommandFactory commandFactory;
        private Function function;
        private boolean embeddable;

        public FunctionDTOBuilder(
                        CommandFactory commandFactory,
                        Function function,
                        boolean embeddable) {
                this.function = function;
                this.commandFactory = commandFactory;
                this.embeddable = embeddable;
        }

        public FunctionDTO build() {
                return EntityFactory.create(FunctionDTO::new, function, builder -> {
                        builder
                                        .with(dto -> dto.setId(function.getId()))
                                        .with(dto -> dto.setKind(function.getKind()))
                                        .with(dto -> dto.setProject(function.getProject()))
                                        .with(dto -> dto.setName(function.getName()))

                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(function.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setSpec(ConversionUtils.reverse(
                                                                                                function.getSpec(),
                                                                                                commandFactory,
                                                                                                "cbor")));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(function.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setExtra(ConversionUtils.reverse(
                                                                                                function.getExtra(),
                                                                                                commandFactory,
                                                                                                "cbor")));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(function.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setCreated(function.getCreated()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(function.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setUpdated(function.getUpdated()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(function.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setEmbedded(function.getEmbedded()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {

                                                Optional.ofNullable(function.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setState(function.getState() == null
                                                                                                ? State.CREATED.name()
                                                                                                : function.getState()
                                                                                                                .name()));

                                        });

                });
        }
}