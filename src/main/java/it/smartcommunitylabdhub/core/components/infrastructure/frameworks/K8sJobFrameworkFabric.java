package it.smartcommunitylabdhub.core.components.infrastructure.frameworks;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.fabric8.kubernetes.api.model.EnvVar;
import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.api.model.batch.v1.Job;
import io.fabric8.kubernetes.api.model.batch.v1.JobBuilder;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.Watch;
import io.fabric8.kubernetes.client.Watcher;
import io.fabric8.kubernetes.client.WatcherException;
import it.smartcommunitylabdhub.core.components.fsm.StateMachine;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunEvent;
import it.smartcommunitylabdhub.core.components.fsm.enums.RunState;
import it.smartcommunitylabdhub.core.components.fsm.types.RunStateMachine;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.frameworks.Framework;
import it.smartcommunitylabdhub.core.components.infrastructure.runnables.K8sJobRunnable;
import it.smartcommunitylabdhub.core.components.kubernetes.EventPrinter;
import it.smartcommunitylabdhub.core.components.kubernetes.K8sJobBuilderHelper;
import it.smartcommunitylabdhub.core.models.builders.log.LogEntityBuilder;
import it.smartcommunitylabdhub.core.models.entities.log.LogDTO;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.services.interfaces.LogService;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

//@FrameworkComponent(framework = "k8sjob_old")
@Log4j2
public class K8sJobFrameworkFabric implements Framework<K8sJobRunnable> {

    //    @Autowired
    KubernetesClient kubernetesClient;

    // @Autowired
    // ApplicationEventPublisher eventPublisher;

    @Autowired
    RunStateMachine runStateMachine;

    @Autowired
    LogEntityBuilder logEntityBuilder;

    @Autowired
    LogService logService;

    @Autowired
    RunService runService;

    @Autowired
    K8sJobBuilderHelper k8sJobBuilderHelper;


    // TODO: instead of void define a Result object that have to be merged with the run from the
    // caller.
    @Override
    public void execute(K8sJobRunnable runnable) {

        // Log service execution initiation
        log.info("----------------- PREPARE KUBERNETES JOB ----------------");

        ObjectMapper objectMapper = new ObjectMapper();

        // FIXME: DELETE THIS IS ONLY FOR DEBUG
        String threadName = Thread.currentThread().getName();

        // Specify the Kubernetes namespace
        final String namespace = "default";


        // Prepare environment variables for the Kubernetes job
        List<EnvVar> envVars = k8sJobBuilderHelper.getEnv();

        // Merge function specific envs
        runnable.getEnvs().entrySet().stream().forEach(entry -> {
            envVars.add(
                    new EnvVar(entry.getKey(), entry.getValue(), null));
        });

        // Generate jobName and ContainerName
        String jobName = getJobName(runnable.getRuntime(), runnable.getTask(), runnable.getId());
        String containerName =
                getContainerName(runnable.getRuntime(), runnable.getTask(), runnable.getId());

        // Create labels for job
        Map<String, String> labels = Map.of(
                "app.kubernetes.io/instance", "dhcore-" + jobName,
                "app.kubernetes.io/version", "0.0.3",
                "app.kubernetes.io/component", "job",
                "app.kubernetes.io/part-of", "dhcore-k8sjob",
                "app.kubernetes.io/managed-by", "dhcore");

        // Build the Kubernetes Job configuration
        Job job = new JobBuilder()
                .withNewMetadata()
                .withName(jobName)
                .withLabels(labels)
                .endMetadata()
                .withNewSpec()
                .withNewTemplate()
                .withNewSpec()
                .addNewContainer()
                .withEnv(envVars)
                .withName(containerName)
                .withImage(runnable.getImage())
                .withImagePullPolicy("IfNotPresent")
                .withCommand(getCommand(runnable))
                .endContainer()
                .withRestartPolicy("Never")
                .endSpec()
                .endTemplate()
                .endSpec()
                .build();


        // Create the Kubernetes Job in the specified namespace
        Job jobResult = kubernetesClient.resource(job).inNamespace(namespace).create();


        // TODO: change this part as a poller instead of a watcher using kubeclient and jobId
        // Initialize the run state machine considering current state and context
        StateMachine<RunState, RunEvent, Map<String, Object>> fsm = runStateMachine
                .create(RunState.valueOf(runnable.getState()),
                        Map.of("runId", runnable.getId()));


        // Log the initiation of Dbt Kubernetes Listener
        log.info("Dbt Kubernetes Listener [" + threadName + "] "
                + jobName
                + "@"
                + namespace);


        // Watch for current job events
        Watch watch = kubernetesClient.v1().events().inAnyNamespace().watch(new Watcher<Event>() {
            @Override
            public void eventReceived(Action action, Event event) {
                try {
                    // Extract involved object information from the event
                    String involvedObjectUid = event.getInvolvedObject().getUid();

                    // if event involved object is equal to the job uuid I created before then
                    // log event
                    if (jobResult.getMetadata().getUid().equals(involvedObjectUid)) {
                        EventPrinter.printEvent(event);

                        String eventJson = objectMapper.writeValueAsString(event);

                        logService.createLog(LogDTO.builder()
                                .run(runnable.getId())
                                .project(runnable.getProject())
                                .body(Map.of("content", eventJson))
                                .build());


                        if (event.getReason().equals("SuccessfulCreate")) {
                            fsm.goToState(RunState.READY);
                            fsm.goToState(RunState.RUNNING);
                        }

                        // when message is completed update run
                        if (event.getReason().equals("Completed")) {
                            fsm.goToState(RunState.COMPLETED);
                            RunDTO runDTO = runService.getRun(runnable.getId());
                            runDTO.setState(fsm.getCurrentState().name());
                            runService.updateRun(runDTO, runDTO.getId());
                        }
                    }
                } catch (Exception e) {
                    log.error(e.getMessage());
                }
            }


            @Override
            public void onClose(WatcherException cause) {
                if (cause != null) {
                    // Handle any KubernetesClientException that occurred during
                    // watch
                    log.error("An error occurred during the Kubernetes events watch: "
                            + cause.getMessage());
                } else {
                    // Handle watch closure
                    log.error("The Kubernetes events watch has been closed.");
                }
            }
        });

        // Wait until job is succeded..this is thread blocking functionality for this reason
        // every watcher is on @Async method.
        kubernetesClient.batch().v1().jobs().inNamespace(namespace)
                .withName(jobName)
                .waitUntilCondition(j -> j.getStatus().getSucceeded() != null
                        && j.getStatus().getSucceeded() > 0, 8L, TimeUnit.HOURS);

        // Get job execution logs
        String jobLogs =
                kubernetesClient.batch().v1().jobs().inNamespace(namespace)
                        .withName(jobName)
                        .getLog();

        // Write job execution logs to the log service
        logService.createLog(LogDTO.builder()
                .run(runnable.getId())
                .project(runnable.getProject())
                .body(Map.of("content", jobLogs))
                .build());


        // Close the job execution watch
        watch.close();

        // Clean up the job
        kubernetesClient.batch().v1().jobs().inNamespace(namespace)
                .withName(jobName)
                .delete();
    }

    // Concat command with arguments
    private String[] getCommand(K8sJobRunnable runnable) {
        return Stream.concat(
                Stream.of(runnable.getCommand()),
                Arrays.stream(runnable.getArgs())).toArray(String[]::new);
    }

    // Generate and return job name
    private String getJobName(String runtime, String task, String id) {
        return "j" + "-" + runtime + "-" + task + "-" + id;
    }

    // Generate and return container name
    private String getContainerName(String runtime, String task, String id) {
        return "c" + "-" + runtime + "-" + task + "-" + id;
    }

}
