package it.smartcommunitylabdhub.core.components.kubernetes;

import java.util.Optional;

import org.springframework.stereotype.Component;
import io.fabric8.kubernetes.api.model.Service;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.fabric8.kubernetes.client.Watch;
import io.fabric8.kubernetes.client.Watcher;
import io.fabric8.kubernetes.client.WatcherException;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import lombok.extern.log4j.Log4j2;

@Component
@Log4j2
public class k8sEventListener {

    private final Optional<KubernetesClient> kubernetesClient;

    private Watch watchEvents;
    private Watch watchService;


    public k8sEventListener(Optional<KubernetesClient> kubernetesClient) {
        this.kubernetesClient = kubernetesClient;
    }

    @PostConstruct
    public void init() {
        try {
            kubernetesClient.ifPresent(kubeClient -> {


                /*
                 * // Watch events on kubernetes watchEvents = kubeClient.v1().events()
                 * .inAnyNamespace() .watch(new Watcher<Event>() {
                 * 
                 * @Override public void eventReceived(Action action, Event resource) {
                 * eventProcessor.processEvent(action, resource); }
                 * 
                 * @Override public void onClose(WatcherException cause) { if (cause != null) { //
                 * Handle any KubernetesClientException that occurred during // watch
                 * System.err.println( "An error occurred during the Kubernetes events watch: " +
                 * cause.getMessage()); } else { // Handle watch closure System.out.println(
                 * "The Kubernetes events watch has been closed."); } }
                 * 
                 * });
                 */

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
