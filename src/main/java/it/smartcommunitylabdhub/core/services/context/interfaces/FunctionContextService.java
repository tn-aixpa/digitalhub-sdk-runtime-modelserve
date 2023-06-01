package it.smartcommunitylabdhub.core.services.context.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;

import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;

public interface FunctionContextService {

        FunctionDTO createFunction(String projectName, FunctionDTO functionDTO);

        List<FunctionDTO> getByProjectNameAndFunctionName(
                        String projectName, String functionName, Pageable pageable);

        List<FunctionDTO> getLatestByProjectName(
                        String projectName, Pageable pageable);

        FunctionDTO getByProjectAndFunctionAndUuid(
                        String projectName, String functionName, String uuid);

        FunctionDTO getLatestByProjectNameAndFunctionName(
                        String projectName, String functionName);

        FunctionDTO createOrUpdateFunction(String projectName, String functionName, FunctionDTO functionDTO);

        FunctionDTO updateFunction(String projectName, String functionName, String uuid, FunctionDTO functionDTO);

        Boolean deleteSpecificFunctionVersion(String projectName, String functionName, String uuid);

        Boolean deleteAllFunctionVersions(String projectName, String functionName);
}
