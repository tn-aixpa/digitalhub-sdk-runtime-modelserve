package it.smartcommunitylabdhub.dbt.components.runners;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import it.smartcommunitylabdhub.core.annotations.infrastructure.RunnerComponent;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables.Runnable;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runners.Runner;
import it.smartcommunitylabdhub.core.components.infrastructure.runnables.K8sJobRunnable;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunUtils;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;


@RunnerComponent(runtime = "dbt", task = "transform")
public class DbtTransformRunner implements Runner {

	@Override
	public Runnable produce(RunDTO runDTO) {

		return Optional.ofNullable(runDTO)
				.map(this::validateRunDTO)
				.orElseThrow(() -> new IllegalArgumentException("Invalid runDTO"));

	}

	@SuppressWarnings("unchecked")
	private K8sJobRunnable validateRunDTO(RunDTO runDTO) {

		// Create accessor
		RunAccessor runAccessor = RunUtils.parseRun(runDTO.getTask());

		// Check for valid parameters image, command and args
		String image = (String) runDTO.getSpec().get("image");
		if (image == null) {
			throw new IllegalArgumentException(
					"Invalid argument: image not found in runDTO spec");
		}

		String command = (String) runDTO.getSpec().get("command");
		if (command == null) {
			throw new IllegalArgumentException(
					"Invalid argument: command not found in runDTO spec");
		}

		List<String> args = (List<String>) runDTO.getSpec().get("args");
		if (args == null) {
			throw new IllegalArgumentException(
					"Invalid argument: args not found in runDTO spec");
		}

		K8sJobRunnable k8sJobRunnable = K8sJobRunnable.builder()
				.runtime(runAccessor.getRuntime())
				.task(runAccessor.getTask())
				.image(image)
				.command(command)
				.args(args.toArray(String[]::new))
				.envs(Map.of(
						"PROJECT_NAME", runDTO.getProject(),
						"RUN_ID", runDTO.getId()))
				.state(runDTO.getState())
				.build();

		k8sJobRunnable.setId(runDTO.getId());
		k8sJobRunnable.setProject(runDTO.getProject());

		return k8sJobRunnable;
	}


}
