package it.smartcommunitylabdhub.core.services.interfaces;

import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import java.util.List;

import org.springframework.data.domain.Pageable;

public interface FunctionService {
    List<FunctionDTO> getFunctions(Pageable pageable);

    List<FunctionDTO> getFunctions();

    FunctionDTO createFunction(FunctionDTO functionDTO);

    FunctionDTO getFunction(String uuid);

    FunctionDTO updateFunction(FunctionDTO functionDTO, String uuid);

    boolean deleteFunction(String uuid);

    List<RunDTO> getFunctionRuns(String uuid);

    List<FunctionDTO> getAllLatestFunctions();
}
