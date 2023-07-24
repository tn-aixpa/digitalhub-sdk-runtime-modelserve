/**
 * KindPublisherFactory.java
 *
 * This class is a factory for managing and providing KindPublishers for different kinds (types).
 */

package it.smartcommunitylabdhub.core.components.kinds.factory.publishers;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import it.smartcommunitylabdhub.core.annotations.RunPublisherComponent;

public class KindPublisherFactory {
    private final Map<String, KindPublisher<?, ?>> publisherMap;

    /**
     * Constructor to create the KindPublisherFactory with a list of KindPublishers.
     *
     * @param publishers The list of KindPublishers to be managed by the factory.
     */
    public KindPublisherFactory(List<KindPublisher<?, ?>> publishers) {
        publisherMap = publishers.stream().collect(Collectors.toMap(this::getTypeFromAnnotation, Function.identity()));
    }

    /**
     * Get the type string from the @RunPublisherComponent annotation for a given
     * KindPublisher.
     *
     * @param publisher The KindPublisher for which to extract the type string.
     * @return The type string extracted from the @RunPublisherComponent annotation.
     * @throws IllegalArgumentException If no @RunPublisherComponent annotation is
     *                                  found for the publisher.
     */
    private String getTypeFromAnnotation(KindPublisher<?, ?> publisher) {
        Class<?> publisherClass = publisher.getClass();
        if (publisherClass.isAnnotationPresent(RunPublisherComponent.class)) {
            RunPublisherComponent annotation = publisherClass.getAnnotation(RunPublisherComponent.class);
            return annotation.type();
        }
        throw new IllegalArgumentException(
                "No @RunPublisherComponent annotation found for publisher: " + publisherClass.getName());
    }

    /**
     * Get the KindPublisher for the given type.
     *
     * @param type The type string representing the specific kind for which to
     *             retrieve the KindPublisher.
     * @param <I>  The input type of the KindPublisher.
     * @param <O>  The output type (published data) of the KindPublisher.
     * @return The KindPublisher for the specified type.
     * @throws IllegalArgumentException If no KindPublisher is found for the given
     *                                  type.
     */
    public <I, O> KindPublisher<I, O> getPublisher(String type) {
        @SuppressWarnings("unchecked")
        KindPublisher<I, O> publisher = (KindPublisher<I, O>) publisherMap.get(type);
        if (publisher == null) {
            throw new IllegalArgumentException("No publisher found for type: " + type);
        }
        return publisher;
    }
}
