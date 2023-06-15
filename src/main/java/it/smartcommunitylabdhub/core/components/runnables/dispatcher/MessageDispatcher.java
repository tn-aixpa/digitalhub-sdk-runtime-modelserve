package it.smartcommunitylabdhub.core.components.runnables.dispatcher;

import org.springframework.context.ApplicationEventPublisher;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.components.runnables.interfaces.Message;
import it.smartcommunitylabdhub.core.components.runnables.interfaces.MessageHandler;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

@Component
public class MessageDispatcher {
    private final ApplicationEventPublisher eventPublisher;
    private final Map<Class<? extends Message>, MessageHandler<?>> handlerMap;

    public MessageDispatcher(ApplicationEventPublisher eventPublisher) {
        this.eventPublisher = eventPublisher;
        this.handlerMap = new HashMap<>();
    }

    @Async
    public <T extends Message> CompletableFuture<Void> dispatch(T message) {
        CompletableFuture<Void> future = new CompletableFuture<>();

        eventPublisher.publishEvent(message);

        CompletableFuture.runAsync(() -> {
            MessageHandler<T> handler = getHandler(message.getClass());
            if (handler != null) {
                handler.handle(message);
            }
        }).whenComplete((result, ex) -> {
            if (ex != null) {
                future.completeExceptionally(ex);
            } else {
                future.complete(result);
            }
        });

        return future;
    }

    public <T extends Message> void registerHandler(Class<T> messageType, MessageHandler<T> handler) {
        handlerMap.put(messageType, handler);
    }

    @SuppressWarnings("unchecked")
    private <T extends Message> MessageHandler<T> getHandler(Class<?> messageType) {
        return (MessageHandler<T>) handlerMap.get(messageType);
    }
}
