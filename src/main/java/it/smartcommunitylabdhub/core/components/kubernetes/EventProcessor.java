package it.smartcommunitylabdhub.core.components.kubernetes;

import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.client.Watcher.Action;

@Component
public class EventProcessor {

    @Async
    public void processEvent(Action action, Event event) {

        System.out.println("--------------------- KUBE EVENT ---------------------");
        System.out.println("Action Name :" + action.name());

        EventPrinter.printEvent(event);
        System.out.println("------------------------------------------------------");
    }
}
