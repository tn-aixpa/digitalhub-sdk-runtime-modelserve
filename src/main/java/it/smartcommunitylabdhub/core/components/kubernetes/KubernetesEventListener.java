package it.smartcommunitylabdhub.core.components.kubernetes;

import java.util.Map;
import java.util.Optional;

import org.springframework.stereotype.Component;
import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.api.model.Pod;
import io.fabric8.kubernetes.api.model.PodList;
import io.fabric8.kubernetes.api.model.Service;
import io.fabric8.kubernetes.api.model.batch.v1.Job;
import io.fabric8.kubernetes.api.model.batch.v1.JobList;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.Watch;
import io.fabric8.kubernetes.client.Watcher;
import io.fabric8.kubernetes.client.WatcherException;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import lombok.extern.log4j.Log4j2;

@Component
@Log4j2
public class KubernetesEventListener {

    private final EventProcessor eventProcessor;

    private final Optional<KubernetesClient> kubernetesClient;

    private Watch watchEvents;
    private Watch watchService;


    public KubernetesEventListener(EventProcessor eventProcessor,
            Optional<KubernetesClient> kubernetesClient) {
        this.eventProcessor = eventProcessor;
        this.kubernetesClient = kubernetesClient;
    }

    @PostConstruct
    public void init() {
        try {
            kubernetesClient.ifPresent(kubeClient -> {

                // Try to retrive job key from events
                watchEvents = kubeClient.v1().events().inAnyNamespace().watch(new Watcher<Event>() {
                    @Override
                    public void eventReceived(Action action, Event event) {
                        // Extract involved object information from the event
                        String involvedObjectName = event.getInvolvedObject().getName();

                        // Filter Jobs based on a label that matches the involved object's name
                        JobList jobList = kubeClient.batch().v1().jobs().inAnyNamespace()
                                .withLabel("job-name", involvedObjectName).list();
                        if (jobList != null && !jobList.getItems().isEmpty()) {
                            Job job = jobList.getItems().get(0);
                            String jobName = job.getMetadata().getName();
                            eventProcessor.processEvent(action, event, jobName);
                        }
                    }

                    @Override
                    public void onClose(WatcherException cause) {
                        if (cause != null) {
                            // Handle any KubernetesClientException that occurred during
                            // watch
                            System.err.println(
                                    "An error occurred during the Kubernetes events watch: "
                                            + cause.getMessage());
                        } else {
                            // Handle watch closure
                            System.out.println(
                                    "The Kubernetes events watch has been closed.");
                        }
                    }
                });


                // Watch services on kubernetes
                watchService = kubeClient.services()
                        .inAnyNamespace()
                        .watch(new Watcher<>() {
                            @Override
                            public void eventReceived(Action action, Service service) {
                                log.info("Service {} {}", action.name(),
                                        service.getMetadata().getName());
                            }

                            @Override
                            public void onClose(WatcherException cause) {
                                if (cause != null) {
                                    // Handle any KubernetesClientException that occurred during
                                    // watch
                                    System.err.println(
                                            "An error occurred during the Kubernetes services watch: "
                                                    + cause.getMessage());
                                } else {
                                    // Handle watch closure
                                    System.out.println(
                                            "The Kubernetes services watch has been closed.");
                                }
                            }
                        });
            });
        } catch (Exception e) {
            System.out.println(
                    "WARNING: Continue without watching kubernetes event. No configuration on .kube found");
        }
    }

    @PreDestroy
    public void cleanup() {
        if (watchEvents != null) {
            watchEvents.close();
        }
        if (watchService != null) {
            watchService.close();
        }
        kubernetesClient.ifPresent(kubeClient -> kubeClient.close());
    }
}
