package it.smartcommunitylabdhub.dbt.components.runnables.events.services;


import java.util.List;
import java.util.Map;
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
import it.smartcommunitylabdhub.core.components.kubernetes.K8sAbstractJobBuilder;
import it.smartcommunitylabdhub.core.components.kubernetes.K8sJobBuilderHelper;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.dbt.components.runnables.events.messages.DbtKubernetesMessage;
import lombok.extern.log4j.Log4j2;

@Service
@Qualifier("DbtService")
@Log4j2
public class DbtServiceImpl extends K8sAbstractJobBuilder implements KindService<Void> {

	@Autowired
	KubernetesClient kubernetesClient;

	@Autowired
	ApplicationEventPublisher eventPublisher;

	@Autowired
	RunStateMachine runStateMachine;

	@Autowired
	K8sJobBuilderHelper k8sJobBuilderHelper;


	@Override
	public Void run(RunDTO runDTO) {

		log.info("----------------- PREPARE KUBERNETES JOB ----------------");
		final String namespace = "default";

		List<EnvVar> envVars = k8sJobBuilderHelper.getEnv();
		envVars.addAll(List.of(new EnvVar("PROJECT_NAME", runDTO.getProject(), null),
				new EnvVar("RUN_ID", runDTO.getId(), null),
				new EnvVar("POSTGRES_USER", "testuser", null),
				new EnvVar("POSTGRES_PASSWORD", "testpassword", null),
				new EnvVar("POSTGRES_DB", "dbt", null),
				new EnvVar("POSTGRES_DB_HOST", "192.168.49.1", null),
				new EnvVar("POSTGRES_PORT", "5433", null)));

		Job job = new JobBuilder()
				.withNewMetadata()
				.withName(getJobName(runDTO))
				.endMetadata()
				.withNewSpec()
				.withNewTemplate()
				.withNewSpec()
				.addNewContainer()
				.withEnv(envVars)
				.withName(getContainerName(runDTO))
				.withImage("ltrubbianifbk/dbt_core:latest")
				.withImagePullPolicy("IfNotPresent")
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
				.k8sJobName(getJobName(runDTO))
				.k8sUuid(jobResult.getMetadata().getUid())
				.build());

		return null;
	}
}
