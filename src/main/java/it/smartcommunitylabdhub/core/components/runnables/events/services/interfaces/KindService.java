package it.smartcommunitylabdhub.core.components.runnables.events.services.interfaces;

import it.smartcommunitylabdhub.core.models.dtos.RunDTO;

public interface KindService<T> {
    T run(RunDTO runDTO);
}
