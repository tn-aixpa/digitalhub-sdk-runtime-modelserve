package it.smartcommunitylabdhub.core.services.builders.dtos;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.DataItemDTO;
import it.smartcommunitylabdhub.core.models.entities.DataItem;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.services.factory.EntityFactory;

public class DataItemDTOBuilder {

        private CommandFactory commandFactory;
        private DataItem dataItem;

        public DataItemDTOBuilder(
                        CommandFactory commandFactory,
                        DataItem dataItem) {
                this.dataItem = dataItem;
                this.commandFactory = commandFactory;
        }

        public DataItemDTO build() {
                return EntityFactory.create(DataItemDTO::new, dataItem, builder -> {
                        builder
                                        .with(dto -> dto.setId(dataItem.getId()))
                                        .with(dto -> dto.setKind(dataItem.getKind()))
                                        .with(dto -> dto.setProject(dataItem.getProject()))
                                        .with(dto -> dto.setName(dataItem.getName()))
                                        .withIf(dataItem.getEmbedded(), dto -> dto.setSpec(ConversionUtils.reverse(
                                                        dataItem.getSpec(),
                                                        commandFactory,
                                                        "cbor")))
                                        .withIf(dataItem.getEmbedded(), dto -> dto.setExtra(ConversionUtils.reverse(
                                                        dataItem.getExtra(),
                                                        commandFactory,
                                                        "cbor")))
                                        .with(dto -> dto.setState(dataItem.getState() == null ? State.CREATED.name()
                                                        : dataItem.getState().name()))
                                        .with(dto -> dto.setCreated(dataItem.getCreated()))
                                        .with(dto -> dto.setUpdated(dataItem.getUpdated()))
                                        .with(dto -> dto.setEmbedded(dataItem.getEmbedded()))
                                        .with(dto -> dto.setState(dataItem.getState() == null ? State.CREATED.name()
                                                        : dataItem.getState().name()));

                });
        }
}