package it.smartcommunitylabdhub.core.models.builders.entities;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.DataItemDTO;
import it.smartcommunitylabdhub.core.models.entities.DataItem;
import it.smartcommunitylabdhub.core.models.enums.State;

public class DataItemEntityBuilder {

        private DataItemDTO dataItemDTO;

        public DataItemEntityBuilder(
                        DataItemDTO dataItemDTO) {
                this.dataItemDTO = dataItemDTO;
        }

        /**
         * Build a dataItem from a dataItemDTO and store extra values as a cbor
         * 
         * @return
         */
        public DataItem build() {
                DataItem dataItem = EntityFactory.combine(
                                ConversionUtils.convert(dataItemDTO, "dataitem"), dataItemDTO,
                                builder -> {
                                        builder
                                                        .with(a -> a.setExtra(
                                                                        ConversionUtils.convert(dataItemDTO.getExtra(),
                                                                                        "cbor")))
                                                        .with(a -> a.setSpec(
                                                                        ConversionUtils.convert(dataItemDTO.getSpec(),
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

                                                                                        "cbor")))
                                                        .with(a -> a.setSpec(
                                                                        ConversionUtils.convert(dataItemDTO.getSpec(),

                                                                                        "cbor")))
                                                        .with(a -> a.setEmbedded(dataItemDTO.getEmbedded()));
                                });
        }
}