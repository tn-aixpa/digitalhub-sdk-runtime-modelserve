package it.smartcommunitylabdhub.core.services.context.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;
import it.smartcommunitylabdhub.core.models.entities.dataitem.DataItemDTO;

public interface DataItemContextService {

        DataItemDTO createDataItem(String projectName, DataItemDTO dataItemDTO);

        List<DataItemDTO> getByProjectNameAndDataItemName(
                        String projectName, String dataItemName, Pageable pageable);

        List<DataItemDTO> getLatestByProjectName(
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
