package it.smartcommunitylabdhub.core.models.builders.dtos;

import java.util.Optional;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.DataItemDTO;
import it.smartcommunitylabdhub.core.models.entities.DataItem;
import it.smartcommunitylabdhub.core.models.enums.State;

public class DataItemDTOBuilder {

        private DataItem dataItem;
        private boolean embeddable;

        public DataItemDTOBuilder(
                        DataItem dataItem,
                        boolean embeddable) {
                this.dataItem = dataItem;
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

                                                                                                "cbor")));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(dataItem.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setExtra(ConversionUtils.reverse(
                                                                                                dataItem.getExtra(),

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