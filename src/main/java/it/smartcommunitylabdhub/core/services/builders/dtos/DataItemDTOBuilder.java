package it.smartcommunitylabdhub.core.services.builders.dtos;

import java.util.Optional;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.DataItemDTO;
import it.smartcommunitylabdhub.core.models.entities.DataItem;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.services.factory.EntityFactory;

public class DataItemDTOBuilder {

        private CommandFactory commandFactory;
        private DataItem dataItem;
        private boolean embeddable;

        public DataItemDTOBuilder(
                        CommandFactory commandFactory,
                        DataItem dataItem,
                        boolean embeddable) {
                this.dataItem = dataItem;
                this.commandFactory = commandFactory;
                this.embeddable = embeddable;
        }

        public DataItemDTO build() {
                return EntityFactory.create(DataItemDTO::new, dataItem, builder -> {
                        builder
                                        .with(dto -> dto.setId(dataItem.getId()))
                                        .with(dto -> dto.setKind(dataItem.getKind()))
                                        .with(dto -> dto.setProject(dataItem.getProject()))
                                        .with(dto -> dto.setName(dataItem.getName()))

                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(dataItem.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setSpec(ConversionUtils.reverse(
                                                                                                dataItem.getSpec(),
                                                                                                commandFactory,
                                                                                                "cbor")));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(dataItem.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setExtra(ConversionUtils.reverse(
                                                                                                dataItem.getExtra(),
                                                                                                commandFactory,
                                                                                                "cbor")));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(dataItem.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setCreated(dataItem.getCreated()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(dataItem.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setUpdated(dataItem.getUpdated()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(dataItem.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setEmbedded(dataItem.getEmbedded()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {

                                                Optional.ofNullable(dataItem.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setState(dataItem.getState() == null
                                                                                                ? State.CREATED.name()
                                                                                                : dataItem.getState()
                                                                                                                .name()));

                                        });
                });
        }
}