package it.smartcommunitylabdhub.core.services.context.interfaces;

import it.smartcommunitylabdhub.core.models.entities.function.Function;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface FunctionContextService {

    Function createFunction(String projectName, Function functionDTO);

    Page<Function> getByProjectNameAndFunctionName(
            String projectName, String functionName, Pageable pageable);

    Page<Function> getLatestByProjectName(
            String projectName, Pageable pageable);

    Function getByProjectAndFunctionAndUuid(
            String projectName, String functionName, String uuid);

    Function getLatestByProjectNameAndFunctionName(
            String projectName, String functionName);

    Function createOrUpdateFunction(String projectName, String functionName,
                                    Function functionDTO);

    Function updateFunction(String projectName, String functionName, String uuid,
                            Function functionDTO);

    Boolean deleteSpecificFunctionVersion(String projectName, String functionName, String uuid);

    Boolean deleteAllFunctionVersions(String projectName, String functionName);
}
