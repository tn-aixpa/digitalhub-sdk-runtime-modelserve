package it.smartcommunitylabdhub.core.components.runnables.config;

import java.lang.reflect.ParameterizedType;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;

import it.smartcommunitylabdhub.core.components.runnables.dispatcher.MessageDispatcher;
import it.smartcommunitylabdhub.core.components.runnables.interfaces.Message;
import it.smartcommunitylabdhub.core.components.runnables.interfaces.MessageHandler;
import jakarta.annotation.PostConstruct;

@Configuration
public class EventListenerConfig {

    @Autowired
    private MessageDispatcher messageDispatcher;

    @Autowired
    private List<MessageHandler<?>> messageHandlers;

    @PostConstruct
    public void registerHandlers() {
        for (MessageHandler<?> handler : messageHandlers) {
            Class<?> messageType = extractMessageType(handler);
            registerHandler(messageType, handler);
        }
    }

    @SuppressWarnings("unchecked")
    private <T extends Message> void registerHandler(Class<?> messageType, MessageHandler<?> handler) {
        messageDispatcher.registerHandler((Class<T>) messageType, (MessageHandler<T>) handler);
    }

    private Class<?> extractMessageType(MessageHandler<?> handler) {
        ParameterizedType parameterizedType = (ParameterizedType) handler.getClass()
                .getGenericInterfaces()[0];
        return (Class<?>) parameterizedType.getActualTypeArguments()[0];
    }
}
