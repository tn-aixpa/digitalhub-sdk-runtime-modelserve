package it.smartcommunitylabdhub.core.models.builders.task;

import it.smartcommunitylabdhub.core.models.entities.task.specs.TaskSpec;
import lombok.extern.log4j.Log4j2;

import java.lang.reflect.Field;
import java.util.Arrays;
import java.util.Map;
import java.util.stream.Collectors;

@Log4j2
public class TaskSpecBuilder {
    public Map<String, Object> getBaseSpec(TaskSpec taskSpec) {
        return Arrays.stream(taskSpec.getClass().getDeclaredFields())
                .peek(field -> field.setAccessible(true))
                .collect(Collectors.toMap(Field::getName, field -> {
                    try {
                        return field.get(taskSpec);
                    } catch (IllegalAccessException e) {
                        log.error(e.getMessage());
                        return null;
                    }
                }))
                .entrySet().stream()
                .filter(entry -> entry.getValue() != null)
                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
    }
}
