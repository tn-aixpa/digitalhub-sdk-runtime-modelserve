package it.smartcommunitylabdhub.core.services.interfaces;

import it.smartcommunitylabdhub.core.models.entities.dataitem.DataItemDTO;
import org.springframework.data.domain.Pageable;

import java.util.List;

public interface DataItemService {
    List<DataItemDTO> getDataItems(Pageable pageable);

    DataItemDTO createDataItem(DataItemDTO dataItemDTO);

    DataItemDTO getDataItem(String uuid);

    DataItemDTO updateDataItem(DataItemDTO dataItemDTO, String uuid);

    boolean deleteDataItem(String uuid);

}
