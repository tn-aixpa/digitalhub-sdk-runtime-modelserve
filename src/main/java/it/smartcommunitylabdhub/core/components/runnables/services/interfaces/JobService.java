package it.smartcommunitylabdhub.core.components.runnables.services.interfaces;

import it.smartcommunitylabdhub.core.models.dtos.RunDTO;

public interface JobService {
    void run(RunDTO runDTO);
}
