package it.smartcommunitylabdhub.core.components.runnables.listeners;

import java.util.concurrent.CompletableFuture;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.annotations.CoreHanlder;
import it.smartcommunitylabdhub.core.components.runnables.events.NuclioMessage;
import it.smartcommunitylabdhub.core.components.runnables.interfaces.MessageHandler;

@Component
@CoreHanlder
public class NuclioEventListener implements MessageHandler<NuclioMessage> {

    @Override
    public CompletableFuture<Void> handle(NuclioMessage message) {
        return CompletableFuture.runAsync(() -> {
            // Handle Nuclio messages asynchronously

            // Process the runDTO or perform any other operations
        });
    }
}