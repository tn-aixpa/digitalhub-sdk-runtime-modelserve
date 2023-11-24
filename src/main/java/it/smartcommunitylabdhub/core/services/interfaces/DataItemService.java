package it.smartcommunitylabdhub.core.services.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;
import it.smartcommunitylabdhub.core.models.entities.dataitem.DataItem;

public interface DataItemService {
    List<DataItem> getDataItems(Pageable pageable);

    DataItem createDataItem(DataItem dataItemDTO);

    DataItem getDataItem(String uuid);

    DataItem updateDataItem(DataItem dataItemDTO, String uuid);

    boolean deleteDataItem(String uuid);

}
