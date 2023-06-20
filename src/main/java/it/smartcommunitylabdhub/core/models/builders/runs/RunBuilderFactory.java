package it.smartcommunitylabdhub.core.models.builders.runs;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import it.smartcommunitylabdhub.core.annotations.RunBuilderComponent;

public class RunBuilderFactory {
    private final Map<String, RunBuilder> builderMap;

    public RunBuilderFactory(List<RunBuilder> builders) {
        builderMap = builders.stream()
                .collect(Collectors.toMap(this::getTypeFromAnnotation, Function.identity()));
    }

    private String getTypeFromAnnotation(RunBuilder builder) {
        Class<?> builderClass = builder.getClass();
        if (builderClass.isAnnotationPresent(RunBuilderComponent.class)) {
            RunBuilderComponent annotation = builderClass.getAnnotation(RunBuilderComponent.class);
            return annotation.type();
        }
        throw new IllegalArgumentException(
                "No @RunBuilderComponent annotation found for builder: " + builderClass.getName());
    }

    public RunBuilder getBuilder(String type) {
        RunBuilder builder = builderMap.get(type);
        if (builder == null) {
            throw new IllegalArgumentException("No builder found for type: " + type);
        }
        return builder;
    }
}