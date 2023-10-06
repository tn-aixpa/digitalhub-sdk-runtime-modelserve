/**
 * BuilderFactory.java
 *
 * This class is a factory for managing and providing Builders (builders).
 */

package it.smartcommunitylabdhub.core.components.infrastructure.factories.builders;


import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import it.smartcommunitylabdhub.core.annotations.BuilderComponent;

public class BuilderFactory {
        private final Map<String, Builder> builderMap;

        /**
         * Constructor to create the BuilderFactory with a list of Builders.
         *
         * @param builders The list of Builders to be managed by the factory.
         */
        public BuilderFactory(List<Builder> builders) {
                builderMap = builders.stream()
                                .collect(Collectors.toMap(this::getBuilderFromAnnotation,
                                                Function.identity()));
        }

        /**
         * Get the platform string from the @BuilderComponent annotation for a given Builder.
         *
         * @param builder The Builder for which to extract the platform string.
         * @return The platform string extracted from the @BuilderComponent annotation.
         * @throws IllegalArgumentException If no @BuilderComponent annotation is found for the
         *         builder.
         */
        private String getBuilderFromAnnotation(Builder builder) {
                Class<?> builderClass = builder.getClass();
                if (builderClass.isAnnotationPresent(BuilderComponent.class)) {
                        BuilderComponent annotation =
                                        builderClass.getAnnotation(BuilderComponent.class);
                        return annotation.runtime() + "+" + annotation.task();
                }
                throw new IllegalArgumentException(
                                "No @BuilderComponent annotation found for builder: "
                                                + builderClass.getName());
        }

        /**
         * Get the Builder for the given platform.
         *
         * @param runtime The builder platform
         * @param task The task
         * @return The Builder for the specified platform.
         * @throws IllegalArgumentException If no Builder is found for the given platform.
         */
        public Builder getBuilder(String runtime, String task) {

                Builder concreteBuilder =
                                (Builder) builderMap.get(runtime + "+" + task);
                if (concreteBuilder == null) {
                        throw new IllegalArgumentException(
                                        "No builder found for name: " + runtime + "+" + task);
                }
                return concreteBuilder;
        }


        public Map<String, Builder> getBuilders(String runtime) {
                return builderMap.entrySet().stream()
                                .filter(entry -> entry.getKey().startsWith(runtime))
                                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));

        }
}
