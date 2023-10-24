package it.smartcommunitylabdhub.core.components.infrastructure.runtimes;

import java.util.Map;
import it.smartcommunitylabdhub.core.annotations.infrastructure.RuntimeComponent;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.Builder;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.BuilderFactory;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runners.Runner;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runners.RunnerFactory;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runtimes.Runtime;
import lombok.Getter;
import lombok.extern.log4j.Log4j2;

@Log4j2
@Getter
public abstract class BaseRuntime implements Runtime {

	private String runtime;

	protected final BuilderFactory builderFactory;
	protected final RunnerFactory runnerFactory;

	protected Map<String, Runner> runners;
	protected Map<String, Builder> builders;

	protected BaseRuntime(BuilderFactory builderFactory, RunnerFactory runnerFactory) {
		this.builderFactory = builderFactory;
		this.runnerFactory = runnerFactory;

		// Retrieve runtime
		// Retrieve the runtime value from the subclass if it has a @RuntimeComponent annotation
		RuntimeComponent runtimeComponentAnnotation =
				getClass().getAnnotation(RuntimeComponent.class);
		if (runtimeComponentAnnotation != null) {
			runtime = runtimeComponentAnnotation.runtime();

			// register all builders and runners
			builders = builderFactory.getBuilders(runtime);
			runners = runnerFactory.getRunners(runtime);

		} else {
			log.warn("No @RuntimeComponent annotation found on the subclass.");
		}
	}


	public Runner getRunner(String task) {
		return runners.get(runtime + "+" + task);
	}

	public Builder getBuilder(String task) {
		return builders.get(runtime + "+" + task);
	}

}
