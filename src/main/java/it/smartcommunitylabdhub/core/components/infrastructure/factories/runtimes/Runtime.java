package it.smartcommunitylabdhub.core.components.infrastructure.factories.runtimes;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables.Runnable;
import it.smartcommunitylabdhub.core.models.base.RunStatus;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;

/**
 * Runtime expose builder, run and parse method
 */
public interface Runtime {
	RunDTO build(FunctionDTO functionDTO, TaskDTO taskDTO, RunDTO inputRunDTO);

	Runnable run(RunDTO runDTO);

	// TODO: parse should get and parse result job for the given runtime.
	RunStatus parse();
}
