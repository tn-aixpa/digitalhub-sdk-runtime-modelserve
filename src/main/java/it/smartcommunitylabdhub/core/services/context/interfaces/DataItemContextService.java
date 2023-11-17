package it.smartcommunitylabdhub.core.services.context.interfaces;

import it.smartcommunitylabdhub.core.models.entities.dataitem.DataItemDTO;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface DataItemContextService {

    DataItemDTO createDataItem(String projectName, DataItemDTO dataItemDTO);

    Page<DataItemDTO> getByProjectNameAndDataItemName(
            String projectName, String dataItemName, Pageable pageable);

    Page<DataItemDTO> getLatestByProjectName(
            String projectName, Pageable pageable);

    DataItemDTO getByProjectAndDataItemAndUuid(
            String projectName, String dataItemName, String uuid);

    DataItemDTO getLatestByProjectNameAndDataItemName(
            String projectName, String dataItemName);

    DataItemDTO createOrUpdateDataItem(String projectName, String dataItemName,
                                       DataItemDTO dataItemDTO);

    DataItemDTO updateDataItem(String projectName, String dataItemName, String uuid,
                               DataItemDTO dataItemDTO);

    Boolean deleteSpecificDataItemVersion(String projectName, String dataItemName, String uuid);

    Boolean deleteAllDataItemVersions(String projectName, String dataItemName);
}
