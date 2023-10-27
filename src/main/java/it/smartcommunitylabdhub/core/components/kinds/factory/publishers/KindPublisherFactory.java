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
import it.smartcommunitylabdhub.core.annotations.olders.RunPublisherComponent;

public class KindPublisherFactory {
    private final Map<String, KindPublisher<?, ?>> publisherMap;

    /**
     * Constructor to create the KindPublisherFactory with a list of KindPublishers.
     *
     * @param publishers The list of KindPublishers to be managed by the factory.
     */
    public KindPublisherFactory(List<KindPublisher<?, ?>> publishers) {
        publisherMap = publishers.stream()
                .collect(Collectors.toMap(this::getPublisherNameFromAnnotation,
                        Function.identity()));
    }

    /**
     * Get the platform string from the @RunPublisherComponent annotation for a given KindPublisher.
     *
     * @param publisher The KindPublisher for which to extract the platform string.
     * @return The platform string extracted from the @RunPublisherComponent annotation.
     * @throws IllegalArgumentException If no @RunPublisherComponent annotation is found for the
     *         publisher.
     */
    private String getPublisherNameFromAnnotation(KindPublisher<?, ?> publisher) {
        Class<?> publisherClass = publisher.getClass();
        if (publisherClass.isAnnotationPresent(RunPublisherComponent.class)) {
            RunPublisherComponent annotation =
                    publisherClass.getAnnotation(RunPublisherComponent.class);
            return annotation.platform() + "+" + annotation.perform();
        }
        throw new IllegalArgumentException(
                "No @RunPublisherComponent annotation found for publisher: "
                        + publisherClass.getName());
    }

    /**
     * Get the KindPublisher for the given platform.
     *
     * @param platform The platform string representing the specific platform for which to retrieve
     *        the KindPublisher.
     * @param perform The perform string representing the specific perform action for a given
     *        platform.
     * @param <I> The input platform of the KindPublisher.
     * @param <O> The output platform (published data) of the KindPublisher.
     * @return The KindPublisher for the specified platform.
     * @throws IllegalArgumentException If no KindPublisher is found for the given platform.
     */
    public <I, O> KindPublisher<I, O> getPublisher(String platform, String perform) {
        @SuppressWarnings("unchecked")
        KindPublisher<I, O> publisher =
                (KindPublisher<I, O>) publisherMap.get(platform + "+" + perform);
        if (publisher == null) {
            throw new IllegalArgumentException(
                    "No publisher found for platform: " + platform + "+" + perform);
        }
        return publisher;
    }
}
