package it.smartcommunitylabdhub.core.components.kubernetes;

import java.util.Optional;

import org.springframework.stereotype.Component;
import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.Watch;
import io.fabric8.kubernetes.client.Watcher;
import io.fabric8.kubernetes.client.WatcherException;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;

@Component
public class KubernetesEventListener {

    private final EventProcessor eventProcessor;

    private final Optional<KubernetesClient> kubernetesClient;

    private Watch watch;

    public KubernetesEventListener(EventProcessor eventProcessor, Optional<KubernetesClient> kubernetesClient) {
        this.eventProcessor = eventProcessor;
        this.kubernetesClient = kubernetesClient;
    }

    @PostConstruct
    public void init() {
        try {
            kubernetesClient.ifPresent(kubeClient -> {

                watch = kubeClient.v1().events().inAnyNamespace().watch(new Watcher<Event>() {

                    @Override
                    public void eventReceived(Action action, Event resource) {
                        eventProcessor.processEvent(action, resource);
                    }

                    @Override
                    public void onClose(WatcherException cause) {
                        if (cause != null) {
                            // Handle any KubernetesClientException that occurred during watch
                            System.err.println("An error occurred during the Kubernetes watch: " + cause.getMessage());
                        } else {
                            // Handle watch closure
                            System.out.println("The Kubernetes watch has been closed.");
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
        if (watch != null) {
            watch.close();
        }
        kubernetesClient.ifPresent(kubeClient -> kubeClient.close());
    }
}