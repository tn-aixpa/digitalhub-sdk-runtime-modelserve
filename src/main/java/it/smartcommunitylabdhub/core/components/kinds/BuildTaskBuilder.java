/**
 * BuildTaskBuilder.java
 *
 * This class implements the KindBuilder interface to build a TaskDTO for the specific kind "build".
 */

package it.smartcommunitylabdhub.core.components.kinds;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;

import it.smartcommunitylabdhub.core.annotations.RunBuilderComponent;
import it.smartcommunitylabdhub.core.components.kinds.factory.builders.KindBuilder;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.models.accessors.utils.TaskUtils;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
import it.smartcommunitylabdhub.core.repositories.TaskRepository;

@RunBuilderComponent(platform = "build", perform = "perform")
public class BuildTaskBuilder implements KindBuilder<TaskDTO, TaskDTO> {
        // Implementation of the builder

        @Autowired
        TaskRepository taskRepository;

        /**
         * Build a TaskDTO for the "build" kind using the input TaskDTO.
         *
         * @param taskDTO The input TaskDTO to be processed for building the TaskDTO.
         * @return The built TaskDTO of the "build" kind.
         * @throws CoreException If the accessor for the TaskDTO is not found, leading to a failure
         *         in building the TaskDTO.
         */
        @Override
        public TaskDTO build(TaskDTO taskDTO) {
                // Use TaskUtils to parse the task and create the TaskAccessor

                return Optional.ofNullable(TaskUtils.parseTask(taskDTO.getFunction()))
                                .map(accessor -> {
                                        // Build the TaskDTO with the parsed task data
                                        return TaskDTO.builder().kind(taskDTO.getKind())
                                                        .project(taskDTO.getProject())
                                                        .function(taskDTO.getFunction())
                                                        .spec(taskDTO.getSpec()).build();
                                })
                                .orElseThrow(() -> new CoreException("TaskAccessorNotFound",
                                                "Cannot create accessor",
                                                HttpStatus.INTERNAL_SERVER_ERROR));

        }
}
