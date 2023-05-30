package it.smartcommunitylabdhub.core.services.interfaces;

import it.smartcommunitylabdhub.core.models.dtos.DataItemDTO;
import it.smartcommunitylabdhub.core.models.entities.DataItem;

import java.util.List;

import org.springframework.data.domain.Pageable;

public interface DataItemService {
    List<DataItemDTO> getDataItems(Pageable pageable);

    DataItemDTO createDataItem(DataItemDTO dataItemDTO);

    DataItemDTO getDataItem(String uuid);

    DataItemDTO updateDataItem(DataItemDTO dataItemDTO, String uuid);

    boolean deleteDataItem(String uuid);

}
