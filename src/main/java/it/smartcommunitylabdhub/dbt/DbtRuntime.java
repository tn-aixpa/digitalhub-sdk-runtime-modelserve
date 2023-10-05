package it.smartcommunitylabdhub.dbt;

import org.springframework.beans.factory.annotation.Autowired;
import it.smartcommunitylabdhub.core.annotations.RuntimeComponent;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.Builder;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.BuilderFactory;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables.Runnable;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runtimes.Runtime;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.dtos.custom.ExecutionDTO;

@RuntimeComponent(runtime = "dbt", task = "job")
public class DbtRuntime implements Runtime {

	@Autowired
	BuilderFactory builderFactory;

	@Override
	public RunDTO builder(FunctionDTO function, TaskDTO task, ExecutionDTO executionDTO) {

		Builder builder = (Builder) builderFactory.getBuilder(
				"dbt",
				"job");

		return builder.build(function, task, executionDTO);
	}


	@Override
	public Runnable runner(RunDTO runDTO) {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException("Unimplemented method 'runner'");
	}

}
