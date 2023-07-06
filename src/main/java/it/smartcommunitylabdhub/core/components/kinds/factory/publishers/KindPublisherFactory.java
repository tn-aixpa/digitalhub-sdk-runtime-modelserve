package it.smartcommunitylabdhub.core.components.kinds.factory.publishers;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import it.smartcommunitylabdhub.core.annotations.RunPublisherComponent;

public class KindPublisherFactory {
    private final Map<String, KindPublisher<?, ?>> publisherMap;

    public KindPublisherFactory(List<KindPublisher<?, ?>> publishers) {
        publisherMap = publishers.stream()
                .collect(Collectors.toMap(this::getTypeFromAnnotation, Function.identity()));
    }

    private String getTypeFromAnnotation(KindPublisher<?, ?> publisher) {
        Class<?> publisherClass = publisher.getClass();
        if (publisherClass.isAnnotationPresent(RunPublisherComponent.class)) {
            RunPublisherComponent annotation = publisherClass.getAnnotation(RunPublisherComponent.class);
            return annotation.type();
        }
        throw new IllegalArgumentException(
                "No @RunPublisherComponent annotation found for publisher: " + publisherClass.getName());
    }

    public <I, O> KindPublisher<I, O> getPublisher(String type) {
        @SuppressWarnings("unchecked")
        KindPublisher<I, O> publisher = (KindPublisher<I, O>) publisherMap.get(type);
        if (publisher == null) {
            throw new IllegalArgumentException("No publisher found for type: " + type);
        }
        return publisher;
    }
}
