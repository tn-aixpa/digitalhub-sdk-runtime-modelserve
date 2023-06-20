package it.smartcommunitylabdhub.core.models.builders.runs;

import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;

@FunctionalInterface
public interface RunBuilder {
    RunDTO build(TaskDTO taskDTO);
}
