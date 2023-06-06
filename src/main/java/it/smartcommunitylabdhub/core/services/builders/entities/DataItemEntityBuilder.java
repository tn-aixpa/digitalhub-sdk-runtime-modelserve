package it.smartcommunitylabdhub.core.services.builders.entities;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.DataItemDTO;
import it.smartcommunitylabdhub.core.models.entities.DataItem;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.services.factory.EntityFactory;

public class DataItemEntityBuilder {

        private CommandFactory commandFactory;
        private DataItemDTO dataItemDTO;

        public DataItemEntityBuilder(
                        CommandFactory commandFactory,
                        DataItemDTO dataItemDTO) {
                this.dataItemDTO = dataItemDTO;
                this.commandFactory = commandFactory;
        }

        /**
         * Build a dataItem from a dataItemDTO and store extra values as a cbor
         * 
         * @return
         */
        public DataItem build() {
                DataItem dataItem = EntityFactory.combine(
                                ConversionUtils.convert(dataItemDTO, commandFactory, "dataitem"), dataItemDTO,
                                builder -> {
                                        builder
                                                        .with(a -> a.setExtra(
                                                                        ConversionUtils.convert(dataItemDTO.getExtra(),
                                                                                        commandFactory,
                                                                                        "cbor")))
                                                        .with(a -> a.setSpec(
                                                                        ConversionUtils.convert(dataItemDTO.getSpec(),
                                                                                        commandFactory,
                                                                                        "cbor")));
                                });

                return dataItem;
        }

        /**
         * Update a dataItem
         * TODO: x because if element is not passed it override causing empty field
         * 
         * @param dataItem
         * @return
         */
        public DataItem update(DataItem dataItem) {
                return EntityFactory.combine(
                                dataItem, dataItemDTO, builder -> {
                                        builder
                                                        .with(a -> a.setKind(dataItemDTO.getKind()))
                                                        .with(a -> a.setProject(dataItemDTO.getProject()))
                                                        .with(a -> a.setState(dataItemDTO.getState() == null
                                                                        ? State.CREATED
                                                                        : State.valueOf(dataItemDTO.getState())))
                                                        .with(a -> a.setExtra(
                                                                        ConversionUtils.convert(dataItemDTO.getExtra(),
                                                                                        commandFactory,
                                                                                        "cbor")))
                                                        .with(a -> a.setSpec(
                                                                        ConversionUtils.convert(dataItemDTO.getSpec(),
                                                                                        commandFactory,
                                                                                        "cbor")))
                                                        .with(a -> a.setEmbedded(dataItemDTO.getEmbedded()));
                                });
        }
}