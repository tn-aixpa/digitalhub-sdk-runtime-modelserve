package it.smartcommunitylabdhub.core.services.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;
import it.smartcommunitylabdhub.core.models.entities.dataitem.DataItemDTO;

public interface DataItemService {
    List<DataItemDTO> getDataItems(Pageable pageable);

    DataItemDTO createDataItem(DataItemDTO dataItemDTO);

    DataItemDTO getDataItem(String uuid);

    DataItemDTO updateDataItem(DataItemDTO dataItemDTO, String uuid);

    boolean deleteDataItem(String uuid);

}
