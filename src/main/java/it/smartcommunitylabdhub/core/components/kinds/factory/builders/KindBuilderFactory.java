/**
 * KindBuilderFactory.java
 *
 * This class is a factory for managing and providing KindBuilders for different kinds (types).
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
        builderMap = builders.stream().collect(Collectors.toMap(this::getTypeFromAnnotation, Function.identity()));
    }

    /**
     * Get the type string from the @RunBuilderComponent annotation for a given
     * KindBuilder.
     *
     * @param builder The KindBuilder for which to extract the type string.
     * @return The type string extracted from the @RunBuilderComponent annotation.
     * @throws IllegalArgumentException If no @RunBuilderComponent annotation is
     *                                  found for the builder.
     */
    private String getTypeFromAnnotation(KindBuilder<?, ?> builder) {
        Class<?> builderClass = builder.getClass();
        if (builderClass.isAnnotationPresent(RunBuilderComponent.class)) {
            RunBuilderComponent annotation = builderClass.getAnnotation(RunBuilderComponent.class);
            return annotation.type();
        }
        throw new IllegalArgumentException(
                "No @RunBuilderComponent annotation found for builder: " + builderClass.getName());
    }

    /**
     * Get the KindBuilder for the given type.
     *
     * @param type The type string representing the specific kind for which to
     *             retrieve the KindBuilder.
     * @param <I>  The input type of the KindBuilder.
     * @param <O>  The output type (kind) of the KindBuilder.
     * @return The KindBuilder for the specified type.
     * @throws IllegalArgumentException If no KindBuilder is found for the given
     *                                  type.
     */
    public <I, O> KindBuilder<I, O> getBuilder(String type) {
        @SuppressWarnings("unchecked")
        KindBuilder<I, O> builder = (KindBuilder<I, O>) builderMap.get(type);
        if (builder == null) {
            throw new IllegalArgumentException("No builder found for type: " + type);
        }
        return builder;
    }
}
