package it.smartcommunitylabdhub.core.components.infrastructure.frameworks;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;
import org.springframework.beans.factory.annotation.Autowired;
import io.fabric8.kubernetes.api.model.EnvVar;
import io.fabric8.kubernetes.api.model.batch.v1.Job;
import io.fabric8.kubernetes.api.model.batch.v1.JobBuilder;
import io.fabric8.kubernetes.client.KubernetesClient;
import it.smartcommunitylabdhub.core.annotations.FrameworkComponent;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.frameworks.Framework;
import it.smartcommunitylabdhub.core.components.infrastructure.runnables.K8sJobRunnable;
import it.smartcommunitylabdhub.core.components.kubernetes.K8sJobBuilderHelper;
import lombok.extern.log4j.Log4j2;

@FrameworkComponent(framework = "k8sjob")
@Log4j2
public class K8sJobFramework implements Framework<K8sJobRunnable> {

	@Autowired
	KubernetesClient kubernetesClient;

	// @Autowired
	// ApplicationEventPublisher eventPublisher;

	// @Autowired
	// RunStateMachine runStateMachine;

	@Autowired
	K8sJobBuilderHelper k8sJobBuilderHelper;


	// TODO: instead of void define a Result object that have to be merged with the run from the
	// caller.
	@Override
	public void execute(K8sJobRunnable runnable) {

		// Log service execution initiation
		log.info("----------------- PREPARE KUBERNETES JOB ----------------");

		// Specify the Kubernetes namespace
		final String namespace = "default";


		// Prepare environment variables for the Kubernetes job
		List<EnvVar> envVars = k8sJobBuilderHelper.getEnv();

		runnable.getEnvs().entrySet().stream().forEach(entry -> {
			envVars.add(
					new EnvVar(entry.getKey(), entry.getValue(), null));
		});

		// Build the Kubernetes Job configuration
		Job job = new JobBuilder()
				.withNewMetadata()
				.withName(getJobName(runnable.getName(), runnable.getId()))
				.endMetadata()
				.withNewSpec()
				.withNewTemplate()
				.withNewSpec()
				.addNewContainer()
				.withEnv(envVars)
				.withName(getContainerName(runnable.getName(), runnable.getId()))
				.withImage(runnable.getImage())
				.withImagePullPolicy("IfNotPresent")
				.withCommand(getCommand(runnable))
				.endContainer()
				.withRestartPolicy("Never")
				.endSpec()
				.endTemplate()
				.endSpec()
				.build();


		// // Initialize the run state machine considering current state and context
		// StateMachine<RunState, RunEvent, Map<String, Object>> fsm = runStateMachine
		// .create(RunState.valueOf(runDTO.getState()), Map.of("runId", runDTO.getId()));


		// Create the Kubernetes Job in the specified namespace
		Job jobResult = kubernetesClient.resource(job).inNamespace(namespace).create();


		// TODO: instead of emit event to watch the job ...just monitor it here.\
		// // Send a message to the Kubernetes event listener
		// eventPublisher.publishEvent(DbtKubernetesMessage.builder()
		// .fsm(fsm)
		// .runDTO(runDTO)
		// .k8sNamespace(namespace)
		// .k8sJobName(getJobName(runDTO))
		// .k8sUuid(jobResult.getMetadata().getUid())
		// .build());
	}

	private String[] getCommand(K8sJobRunnable runnable) {
		return Stream.concat(
				Stream.of(runnable.getCommand()),
				Arrays.stream(runnable.getArgs())).toArray(String[]::new);
	}

	private String getJobName(String name, String id) {
		return "job" + "-" + name + "-" + id;
	}

	private String getContainerName(String name, String id) {
		return "container-job-" + name + "-" + id;
	}
}
