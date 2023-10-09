package it.smartcommunitylabdhub.core.components.infrastructure.factories.runtimes;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables.Runnable;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;

/**
 * Runtime expose builder and run method
 */
public interface Runtime {
	RunDTO build(FunctionDTO functionDTO, TaskDTO taskDTO, RunDTO inputRunDTO);

	Runnable run(RunDTO runDTO);
}
