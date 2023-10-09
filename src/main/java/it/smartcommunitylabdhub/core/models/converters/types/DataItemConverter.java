package it.smartcommunitylabdhub.core.models.converters.types;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.entities.dataitem.DataItem;
import it.smartcommunitylabdhub.core.models.entities.dataitem.DataItemDTO;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class DataItemConverter implements Converter<DataItemDTO, DataItem> {

    @Override
    public DataItem convert(DataItemDTO dataItemDTO) throws CustomException {
        return DataItem.builder()
                .id(dataItemDTO.getId())
                .name(dataItemDTO.getName())
                .kind(dataItemDTO.getKind())
                .project(dataItemDTO.getProject())
                .embedded(dataItemDTO.getEmbedded())
                .state(dataItemDTO.getState() == null ? State.CREATED
                        : State.valueOf(dataItemDTO.getState()))
                .build();
    }

    @Override
    public DataItemDTO reverseConvert(DataItem dataItem) throws CustomException {
        return DataItemDTO.builder()
                .id(dataItem.getId())
                .name(dataItem.getName())
                .kind(dataItem.getKind())
                .project(dataItem.getProject())
                .embedded(dataItem.getEmbedded())
                .state(dataItem.getState() == null ? State.CREATED.name()
                        : dataItem.getState().name())
                .created(dataItem.getCreated())
                .updated(dataItem.getUpdated())
                .build();
    }

}
