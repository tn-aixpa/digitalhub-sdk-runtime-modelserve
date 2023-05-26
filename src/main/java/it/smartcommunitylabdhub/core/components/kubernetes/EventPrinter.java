package it.smartcommunitylabdhub.core.components.kubernetes;

import io.fabric8.kubernetes.api.model.Event;

public class EventPrinter {

    public static void printEvent(Event event) {
        System.out.println("Event Name: " + event.getMetadata().getName());
        System.out.println("Event Namespace: " + event.getMetadata().getNamespace());
        System.out.println("Event Reason: " + event.getReason());
        System.out.println("Event Message: " + event.getMessage());
        System.out.println("Event Type: " + event.getType());
        System.out.println("First Timestamp: " + event.getFirstTimestamp());
        System.out.println("Last Timestamp: " + event.getLastTimestamp());
        System.out.println("Event Count: " + event.getCount());
        System.out.println("Involved Object:");
        System.out.println("  Kind: " + event.getInvolvedObject().getKind());
        System.out.println("  Name: " + event.getInvolvedObject().getName());
        System.out.println("  Namespace: " + event.getInvolvedObject().getNamespace());
        System.out.println("  UID: " + event.getInvolvedObject().getUid());
    }
}
