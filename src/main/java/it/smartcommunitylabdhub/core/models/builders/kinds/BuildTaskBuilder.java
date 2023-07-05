package it.smartcommunitylabdhub.core.models.builders.kinds;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;

import it.smartcommunitylabdhub.core.annotations.RunBuilderComponent;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.builders.kinds.factory.KindBuilder;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.repositories.TaskRepository;

@RunBuilderComponent(type = "build")
public class BuildTaskBuilder implements KindBuilder<TaskDTO, TaskDTO> {
        // Implementation of the builder

        @Autowired
        TaskRepository taskRepository;

        @Override
        public TaskDTO build(TaskDTO taskDTO) {
                // 1. get function get if exist otherwise throw exeception.

                return Optional.ofNullable(TaskUtils.parseTask(taskDTO.getTask())).map(
                                accessor -> {
                                        return TaskDTO.builder()
                                                        .kind(taskDTO.getKind())
                                                        .project(taskDTO.getProject())
                                                        .task(taskDTO.getTask())
                                                        .spec(taskDTO.getSpec())
                                                        .build();
                                }).orElseThrow(() -> new CoreException("TaskAccessorNotFound", "Cannot create accessor",
                                                HttpStatus.INTERNAL_SERVER_ERROR));

        }
}