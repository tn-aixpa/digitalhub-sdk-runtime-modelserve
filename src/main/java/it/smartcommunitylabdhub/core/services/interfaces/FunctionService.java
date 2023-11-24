package it.smartcommunitylabdhub.core.services.interfaces;

import it.smartcommunitylabdhub.core.models.entities.function.Function;
import it.smartcommunitylabdhub.core.models.entities.run.Run;
import java.util.List;

import org.springframework.data.domain.Pageable;

public interface FunctionService {
    List<Function> getFunctions(Pageable pageable);

    List<Function> getFunctions();

    Function createFunction(Function functionDTO);

    Function getFunction(String uuid);

    Function updateFunction(Function functionDTO, String uuid);

    boolean deleteFunction(String uuid);

    List<Run> getFunctionRuns(String uuid);

    List<Function> getAllLatestFunctions();
}
