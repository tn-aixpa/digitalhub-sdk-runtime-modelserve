package it.smartcommunitylabdhub.core.components.runnables.listeners;

import java.util.concurrent.CompletableFuture;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.annotations.CoreHanlder;
import it.smartcommunitylabdhub.core.components.runnables.events.ServingMessage;
import it.smartcommunitylabdhub.core.components.runnables.interfaces.MessageHandler;

@Component
@CoreHanlder
public class ServingEventListener implements MessageHandler<ServingMessage> {

    @Override
    public CompletableFuture<Void> handle(ServingMessage message) {
        return CompletableFuture.runAsync(() -> {
            // Handle Serving messages asynchronously

            // Process the runDTO or perform any other operations
        });
    }
}