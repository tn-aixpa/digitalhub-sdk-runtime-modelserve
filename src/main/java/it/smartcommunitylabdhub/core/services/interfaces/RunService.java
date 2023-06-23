package it.smartcommunitylabdhub.core.services.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;

import it.smartcommunitylabdhub.core.models.dtos.ExtraDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;

public interface RunService {

    List<RunDTO> getRuns(Pageable pageable);

    RunDTO getRun(String uuid);

    boolean deleteRun(String uuid);

    RunDTO createRun(TaskDTO taskDTO);

    RunDTO executeRun(String uuid, ExtraDTO extraDTO);

    RunDTO save(RunDTO runDTO);

}
