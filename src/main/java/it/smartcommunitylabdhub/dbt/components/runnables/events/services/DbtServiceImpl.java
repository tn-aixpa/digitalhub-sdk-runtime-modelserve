package it.smartcommunitylabdhub.dbt.components.runnables.events.services;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import io.fabric8.kubernetes.api.model.EnvVar;
import io.fabric8.kubernetes.api.model.batch.v1.Job;
import io.fabric8.kubernetes.api.model.batch.v1.JobBuilder;
import io.fabric8.kubernetes.client.KubernetesClient;
import it.smartcommunitylabdhub.core.components.events.services.interfaces.KindService;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import lombok.extern.log4j.Log4j2;

@Service
@Qualifier("DbtService")
@Log4j2
public class DbtServiceImpl implements KindService<Void> {

	@Autowired
	KubernetesClient kubernetesClient;

	@Override
	public Void run(RunDTO runDTO) {

		log.info("-----------------  PREPARE KUBERNETES JOB ----------------");

		TaskAccessor taskAccessor = TaskUtils.parseTask(runDTO.getTask());

		Job job = new JobBuilder()
				.withNewMetadata()
				.withName("job" + "-" + taskAccessor.getKind() + "-"
						+ runDTO.getId())
				.endMetadata()
				.withNewSpec()
				.withNewTemplate()
				.withNewSpec()
				.addNewContainer()
				.withEnv(List.of(
						new EnvVar("DH_CORE", "http://192.168.49.1:8080", null),
						new EnvVar("RUN_ID", runDTO.getId(), null),
						new EnvVar("POSTGRES_USER", "testuser", null),
						new EnvVar("POSTGRES_PASSWORD", "testpassword", null),
						new EnvVar("POSTGRES_DB", "dbt", null),
						new EnvVar("POSTGRES_DB_HOST", "192.168.49.1", null),
						new EnvVar("POSTGRES_PORT", "5433", null)))
				.withName("container-job-" + "-" + taskAccessor.getKind() + "-"
						+ runDTO.getId())
				.withImage("ltrubbianifbk/dbt_core:latest")
				.withCommand("python", "dbt_wrapper.py")
				.endContainer()
				.withRestartPolicy("Never")
				.endSpec()
				.endTemplate()
				.endSpec()
				.build();

		kubernetesClient.resource(job).inNamespace("default").create();

		String jobLogs = kubernetesClient.batch().v1().jobs().inNamespace("default")
				.withName("job" + "-" + taskAccessor.getKind() + "-"
						+ runDTO.getId())
				.getLog();

		System.out.println(jobLogs);

		// Clean up job
		kubernetesClient.batch().v1().jobs().inNamespace("default")
				.withName("job" + "-" + taskAccessor.getKind() + "-"
						+ runDTO.getId())
				.delete();

		return null;
	}
}
