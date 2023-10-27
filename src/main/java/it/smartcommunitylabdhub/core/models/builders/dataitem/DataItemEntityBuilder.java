package it.smartcommunitylabdhub.core.models.builders.dataitem;

import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.entities.dataitem.DataItem;
import it.smartcommunitylabdhub.core.models.entities.dataitem.DataItemDTO;
import it.smartcommunitylabdhub.core.models.enums.State;
import org.springframework.stereotype.Component;

@Component
public class DataItemEntityBuilder {

    /**
     * Build d dataItem from d dataItemDTO and store extra values as d cbor
     *
     * @return
     */
    public DataItem build(DataItemDTO dataItemDTO) {
        return EntityFactory.combine(
                ConversionUtils.convert(dataItemDTO, "dataitem"), dataItemDTO,
                builder -> builder
                        .with(d -> d.setMetadata(
                                ConversionUtils.convert(dataItemDTO
                                                .getMetadata(),
                                        "metadata")))
                        .with(d -> d.setExtra(
                                ConversionUtils.convert(dataItemDTO
                                                .getExtra(),
                                        "cbor")))
                        .with(d -> d.setSpec(
                                ConversionUtils.convert(dataItemDTO
                                                .getSpec(),
                                        "cbor"))));

    }

    /**
     * Update d dataItem if element is not passed it override causing empty field
     *
     * @param dataItem
     * @return
     */
    public DataItem update(DataItem dataItem, DataItemDTO dataItemDTO) {
        return EntityFactory.combine(
                dataItem, dataItemDTO, builder -> builder
                        .with(d -> d.setKind(dataItemDTO.getKind()))
                        .with(d -> d.setProject(dataItemDTO.getProject()))
                        .with(d -> d.setState(dataItemDTO.getState() == null
                                ? State.CREATED
                                : State.valueOf(dataItemDTO
                                .getState())))

                        .with(d -> d.setMetadata(
                                ConversionUtils.convert(dataItemDTO
                                                .getMetadata(),
                                        "metadata")))
                        .with(d -> d.setExtra(
                                ConversionUtils.convert(dataItemDTO
                                                .getExtra(),

                                        "cbor")))
                        .with(d -> d.setSpec(
                                ConversionUtils.convert(dataItemDTO
                                                .getSpec(),

                                        "cbor")))
                        .with(d -> d.setEmbedded(
                                dataItemDTO.getEmbedded())));
    }
}
