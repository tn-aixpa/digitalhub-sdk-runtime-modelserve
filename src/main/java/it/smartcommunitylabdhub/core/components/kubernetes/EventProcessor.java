package it.smartcommunitylabdhub.core.components.kubernetes;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.client.Watcher.Action;

@Component
public class EventProcessor {

    @Autowired
    EventLogger eventLogger;

    @Async
    public void processEvent(Action action, Event event) {

        System.out.println("--------------------- KUBE EVENT ---------------------");
        System.out.println("Action Name :" + action.name());

        EventPrinter.printEvent(event);

        eventLogger.logEvent(event);

        System.out.println("------------------------------------------------------");
    }
}
