package it.smartcommunitylabdhub.core.components.runnables.services.interfaces;

import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;

public interface JobService {
    void run(RunDTO runDTO, TaskDTO taskDTO);
}
