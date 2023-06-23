package it.smartcommunitylabdhub.core.components.runnables.events.services.interfaces;

import it.smartcommunitylabdhub.core.models.dtos.RunDTO;

public interface JobService<T> {
    T run(RunDTO runDTO);
}
