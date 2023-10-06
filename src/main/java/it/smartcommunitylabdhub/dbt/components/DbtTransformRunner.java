package it.smartcommunitylabdhub.dbt.components;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import io.fabric8.kubernetes.api.model.EnvVar;
import it.smartcommunitylabdhub.core.annotations.RunnerComponent;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables.Runnable;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runners.Runner;
import it.smartcommunitylabdhub.core.components.infrastructure.runnables.K8sJobRunnable;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;


@RunnerComponent(runtime = "dbt", task = "transform")
public class DbtTransformRunner implements Runner {

	@Override
	public Runnable produce(RunDTO runDTO) {

		@SuppressWarnings("unchecked")
		K8sJobRunnable k8sJobRunnable = K8sJobRunnable.builder()
				.name((String) runDTO.getSpec().get("name"))
				.image((String) runDTO.getSpec().get("image"))
				.command((String) runDTO.getSpec().get("command"))
				.args(((List<String>) runDTO.getSpec().get("args"))
						.toArray(String[]::new))
				.envs(Map.of(
						"PROJECT_NAME", runDTO.getProject(),
						"RUN_ID", runDTO.getId()))
				.build();

		k8sJobRunnable.setId(runDTO.getId());
		k8sJobRunnable.setProject(runDTO.getProject());

		return k8sJobRunnable;
	}


}
