package it.smartcommunitylabdhub.core.components.infrastructure.factories.runtimes;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables.Runnable;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.dtos.custom.ExecutionDTO;

/**
 * Runtime expose builder and run method
 */
public interface Runtime {
	RunDTO build(FunctionDTO functionDTO, TaskDTO taskDTO, ExecutionDTO executionDTO);

	Runnable run(RunDTO runDTO);
}
