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


/**
 * DbtServiceImpl.java
 *
 * This service class is responsible for preparing and running Kubernetes jobs for the Dbt (Data
 * Build Tool) service.
 *
 * It constructs a Kubernetes Job with specific environment variables and settings, initiates a
 * State Machine to manage the state of the Dbt job, and publishes events related to the job's
 * execution.
 *
 */
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


	/**
	 * Run a Dbt job in a Kubernetes cluster.
	 *
	 * @param runDTO The RunDTO containing job details.
	 * @return {@code null} (void method)
	 */
	@Override
	public Void run(RunDTO runDTO) {

		// Log service execution initiation
		log.info("----------------- PREPARE KUBERNETES JOB ----------------");

		// Specify the Kubernetes namespace
		final String namespace = "default";


		// Prepare environment variables for the Kubernetes job
		List<EnvVar> envVars = k8sJobBuilderHelper.getEnv();
		envVars.addAll(List.of(
				new EnvVar("PROJECT_NAME", runDTO.getProject(), null),
				new EnvVar("RUN_ID", runDTO.getId(), null),
				new EnvVar("S3_ENDPOINT_URL", "http://192.168.49.2:30080", null),
				new EnvVar("S3_ACCESS_KEY_ID", "minio", null),
				new EnvVar("S3_SECRET_ACCESS_KEY", "minio123", null),
				new EnvVar("S3_BUCKET_NAME", "mlrun", null),
				new EnvVar("POSTGRES_HOST", "192.168.49.1", null),
				new EnvVar("POSTGRES_PORT", "5433", null),
				new EnvVar("POSTGRES_DB", "dbt", null),
				new EnvVar("POSTGRES_USER", "testuser", null),
				new EnvVar("POSTGRES_PASSWORD", "testpassword", null),
				new EnvVar("POSTGRES_SCHEMA", "public", null)));

		// Build the Kubernetes Job configuration
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


		// Initialize the run state machine considering current state and context
		StateMachine<RunState, RunEvent, Map<String, Object>> fsm = runStateMachine
				.create(RunState.valueOf(runDTO.getState()), Map.of("runId", runDTO.getId()));


		// Create the Kubernetes Job in the specified namespace
		Job jobResult = kubernetesClient.resource(job).inNamespace(namespace).create();

		// Send a message to the Kubernetes event listener
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
