package it.smartcommunitylabdhub.core.components.kubernetes;

import java.util.List;
import io.fabric8.kubernetes.api.model.EnvVar;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;

public interface K8sJobBuilderHelper {

	public default List<EnvVar> getEnv(RunDTO runDTO) {
		return List.of(
				new EnvVar("DHUB_CORE_ENDPOINT", "http://192.168.49.1:8080", null),
				new EnvVar("RUN_ID", runDTO.getId(), null),
				new EnvVar("POSTGRES_USER", "testuser", null),
				new EnvVar("POSTGRES_PASSWORD", "testpassword", null),
				new EnvVar("POSTGRES_DB", "dbt", null),
				new EnvVar("POSTGRES_DB_HOST", "192.168.49.1", null),
				new EnvVar("POSTGRES_PORT", "5433", null),
				new EnvVar("AWS_ACCESS_KEY_ID", "minio", null),
				new EnvVar("AWS_SECRET_ACCESS_KEY", "minio123", null),
				new EnvVar("S3_ENDPOINT", "http://192.168.49.2:30080", null),
				new EnvVar("PROJECT_NAME", runDTO.getProject(), null));
	}

	public default TaskAccessor getTaskAccessor(RunDTO runDTO) {
		return TaskUtils.parseTask(runDTO.getTask());
	}


	public default String getJobName(RunDTO runDTO) {
		return "job" + "-" + getTaskAccessor(runDTO).getKind() + "-" + runDTO.getId();
	}

	public default String getContainerName(RunDTO runDTO) {
		return "container-job-" + getTaskAccessor(runDTO).getKind() + "-" + runDTO.getId();
	}

}
