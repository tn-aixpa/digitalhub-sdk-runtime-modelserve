package it.smartcommunitylabdhub.dbt.components.runnables.events.services;


import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;

import io.fabric8.kubernetes.api.model.EnvVar;
import io.fabric8.kubernetes.api.model.batch.v1.Job;
import io.fabric8.kubernetes.api.model.batch.v1.JobBuilder;
import io.fabric8.kubernetes.client.KubernetesClient;
import it.smartcommunitylabdhub.core.components.events.services.interfaces.KindService;
import it.smartcommunitylabdhub.core.components.fsm.StateMachine;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunEvent;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunState;
import it.smartcommunitylabdhub.core.components.fsm.types.RunStateMachine;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.dbt.components.runnables.events.messages.DbtKubernetesMessage;
import lombok.extern.log4j.Log4j2;

@Service
@Qualifier("DbtService")
@Log4j2
public class DbtServiceImpl implements KindService<Void> {

	@Autowired
	KubernetesClient kubernetesClient;

	@Autowired
	ApplicationEventPublisher eventPublisher;

	@Autowired
	RunStateMachine runStateMachine;


	@Override
	public Void run(RunDTO runDTO) {

		log.info("-----------------  PREPARE KUBERNETES JOB ----------------");

		final TaskAccessor taskAccessor = TaskUtils.parseTask(runDTO.getTask());
		final String namespace = "default";
		final String jobName = "job" + "-" + taskAccessor.getKind() + "-"
				+ runDTO.getId();


		Job job = new JobBuilder()
				.withNewMetadata()
				.withName(jobName)
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
				.withName("container-job-" + taskAccessor.getKind() + "-"
						+ runDTO.getId())
				.withImage("ltrubbianifbk/dbt_core:latest")
				.withCommand("python", "dbt_wrapper.py")
				.endContainer().withRestartPolicy("Never")
				.endSpec()
				.endTemplate()
				.endSpec()
				.build();


		// Init run state machine considering current state and context.
		StateMachine<RunState, RunEvent, Map<String, Object>> fsm = runStateMachine
				.create(RunState.valueOf(runDTO.getState()), Map.of("runId", runDTO.getId()));


		// Create Job in k8s
		Job jobResult = kubernetesClient.resource(job).inNamespace(namespace).create();

		// Send message to k8s event listener
		eventPublisher.publishEvent(DbtKubernetesMessage.builder()
				.fsm(fsm)
				.runDTO(runDTO)
				.k8sNamespace(namespace)
				.k8sJobName(jobName)
				.k8sUuid(jobResult.getMetadata().getUid())
				.build());

		return null;
	}
}
