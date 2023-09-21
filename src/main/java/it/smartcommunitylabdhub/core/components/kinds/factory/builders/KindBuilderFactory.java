/**
 * KindBuilderFactory.java
 *
 * This class is a factory for managing and providing KindBuilders for different platforms
 * (platforms).
 */

package it.smartcommunitylabdhub.core.components.kinds.factory.builders;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import it.smartcommunitylabdhub.core.annotations.RunBuilderComponent;

public class KindBuilderFactory {
    private final Map<String, KindBuilder<?, ?>> builderMap;

    /**
     * Constructor to create the KindBuilderFactory with a list of KindBuilders.
     *
     * @param builders The list of KindBuilders to be managed by the factory.
     */
    public KindBuilderFactory(List<KindBuilder<?, ?>> builders) {
        builderMap = builders.stream()
                .collect(Collectors.toMap(this::getBuilderNameFromAnnotation, Function.identity()));
    }

    /**
     * Get the platform string from the @RunBuilderComponent annotation for a given KindBuilder.
     *
     * @param builder The KindBuilder for which to extract the platform string.
     * @return The platform string extracted from the @RunBuilderComponent annotation.
     * @throws IllegalArgumentException If no @RunBuilderComponent annotation is found for the
     *         builder.
     */
    private String getBuilderNameFromAnnotation(KindBuilder<?, ?> builder) {
        Class<?> builderClass = builder.getClass();
        if (builderClass.isAnnotationPresent(RunBuilderComponent.class)) {
            RunBuilderComponent annotation = builderClass.getAnnotation(RunBuilderComponent.class);
            return annotation.platform() + "+" + annotation.perform();
        }
        throw new IllegalArgumentException(
                "No @RunBuilderComponent annotation found for builder: " + builderClass.getName());
    }

    /**
     * Get the KindBuilder for the given platform.
     *
     * @param platform The platform string representing the specific platform for which to retrieve
     *        the KindBuilder.
     * @param perform The perform string representing the specific perform action for a given
     *        platform.
     * @param <I> The input platform of the KindBuilder.
     * @param <O> The output platform (platform) of the KindBuilder.
     * @return The KindBuilder for the specified platform.
     * @throws IllegalArgumentException If no KindBuilder is found for the given platform.
     */
    public <I, O> KindBuilder<I, O> getBuilder(String platform, String perform) {
        @SuppressWarnings("unchecked")
        KindBuilder<I, O> builder =
                (KindBuilder<I, O>) builderMap.get(platform + "+" + perform);
        if (builder == null) {
            throw new IllegalArgumentException(
                    "No builder found for name: " + platform + "+" + perform);
        }
        return builder;
    }
}
