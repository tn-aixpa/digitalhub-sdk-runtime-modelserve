package it.smartcommunitylabdhub.dbt.components.runtimes;

import it.smartcommunitylabdhub.core.annotations.RuntimeComponent;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.Builder;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.BuilderFactory;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables.Runnable;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runners.Runner;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runners.RunnerFactory;
import it.smartcommunitylabdhub.core.components.infrastructure.runtimes.BaseRuntime;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunUtils;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
import it.smartcommunitylabdhub.core.models.shared.RunStatus;

@RuntimeComponent(runtime = "dbt")
public class DbtRuntime extends BaseRuntime {

	public DbtRuntime(BuilderFactory builderFactory, RunnerFactory runnerFactory) {
		super(builderFactory, runnerFactory);
	}


	@Override
	public RunDTO build(FunctionDTO function, TaskDTO task, RunDTO inputRunDTO) {
		Builder builder = getBuilder(task.getKind());
		return builder.build(function, task, inputRunDTO);
	}


	@Override
	public Runnable run(RunDTO runDTO) {
		RunAccessor runAccessor = RunUtils.parseRun(runDTO.getTask());
		Runner runner = getRunner(runAccessor.getTask());
		return runner.produce(runDTO);
	}


	@Override
	public RunStatus parse() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException("Unimplemented method 'parse'");
	}

}
