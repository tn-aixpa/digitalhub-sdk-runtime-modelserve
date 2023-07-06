package it.smartcommunitylabdhub.core.components.kinds.factory.builders;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import it.smartcommunitylabdhub.core.annotations.RunBuilderComponent;

public class KindBuilderFactory {
    private final Map<String, KindBuilder<?, ?>> builderMap;

    public KindBuilderFactory(List<KindBuilder<?, ?>> builders) {
        builderMap = builders.stream()
                .collect(Collectors.toMap(this::getTypeFromAnnotation, Function.identity()));
    }

    private String getTypeFromAnnotation(KindBuilder<?, ?> builder) {
        Class<?> builderClass = builder.getClass();
        if (builderClass.isAnnotationPresent(RunBuilderComponent.class)) {
            RunBuilderComponent annotation = builderClass.getAnnotation(RunBuilderComponent.class);
            return annotation.type();
        }
        throw new IllegalArgumentException(
                "No @RunBuilderComponent annotation found for builder: " + builderClass.getName());
    }

    public <I, O> KindBuilder<I, O> getBuilder(String type) {
        @SuppressWarnings("unchecked")
        KindBuilder<I, O> builder = (KindBuilder<I, O>) builderMap.get(type);
        if (builder == null) {
            throw new IllegalArgumentException("No builder found for type: " + type);
        }
        return builder;
    }
}
