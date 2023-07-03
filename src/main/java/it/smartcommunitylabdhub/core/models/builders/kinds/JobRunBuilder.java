package it.smartcommunitylabdhub.core.models.builders.kinds;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;

import it.smartcommunitylabdhub.core.annotations.RunBuilderComponent;
import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.models.builders.kinds.factory.KindBuilder;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.repositories.TaskRepository;

@RunBuilderComponent(type = "job")
public class JobRunBuilder implements KindBuilder<TaskDTO, RunDTO> {
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
                                                        .kind(task.getKind())
                                                        .taskId(task.getId())
                                                        .project(task.getProject())
                                                        .task(task.getTask())
                                                        .spec(taskDTO.getSpec())
                                                        .build();

                                }).orElseThrow(() -> new CoreException(
                                                "FunctionNotFound",
                                                "The function you are searching for does not exist.",
                                                HttpStatus.NOT_FOUND));

        }
}