package it.smartcommunitylabdhub.core.components.runnables.interfaces;

import java.util.concurrent.CompletableFuture;

@FunctionalInterface
public interface MessageHandler<T extends Message> {
    CompletableFuture<Void> handle(T message);
}
