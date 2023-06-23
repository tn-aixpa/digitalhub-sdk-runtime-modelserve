package it.smartcommunitylabdhub.core.models.builders.runs.kinds;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;

import it.smartcommunitylabdhub.core.annotations.RunBuilderComponent;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.models.builders.runs.RunBuilder;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.repositories.TaskRepository;

@RunBuilderComponent(type = "job")
public class JobRunBuilder implements RunBuilder {
        // Implementation of the builder

        @Autowired
        TaskRepository taskRepository;

        @Override
        public RunDTO build(TaskDTO taskDTO) {
                // 1. get function get if exist otherwise throw exeception.
                return taskRepository.findById(taskDTO.getId())
                                .map(task -> {
                                        // 3. produce a run object and store it
                                        return RunDTO.builder()
                                                        .type(task.getType())
                                                        .taskId(task.getId())
                                                        .project(task.getProject())
                                                        .name(task.getName())
                                                        .spec(taskDTO.getSpec())
                                                        .build();

                                }).orElseThrow(() -> new CoreException(
                                                "FunctionNotFound",
                                                "The function you are searching for does not exist.",
                                                HttpStatus.NOT_FOUND));

        }
}