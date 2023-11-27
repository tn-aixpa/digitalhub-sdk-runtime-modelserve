package it.smartcommunitylabdhub.core.services.interfaces;

import it.smartcommunitylabdhub.core.models.entities.function.specs.FunctionBaseSpec;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import jakarta.validation.Valid;
import org.springframework.data.domain.Pageable;

import java.util.List;

public interface RunService {

    List<RunDTO> getRuns(Pageable pageable);

    RunDTO getRun(String uuid);

    boolean deleteRun(String uuid);

    RunDTO save(RunDTO runDTO);

    <F extends FunctionBaseSpec<F>> RunDTO createRun(RunDTO inputRunDTO);

    RunDTO updateRun(@Valid RunDTO runDTO, String uuid);

}
