package it.smartcommunitylabdhub.core.components.events.services.interfaces;

import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;

public interface KindService<T> {
    T run(RunDTO runDTO);
}
