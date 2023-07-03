package it.smartcommunitylabdhub.core.models.converters.types;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.Task;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class TaskConverter implements Converter<TaskDTO, Task> {

    @Override
    public Task convert(TaskDTO TaskDTO) throws CustomException {
        return Task.builder()
                .id(TaskDTO.getId())
                .task(TaskDTO.getTask())
                .kind(TaskDTO.getKind())
                .project(TaskDTO.getProject())
                .state(TaskDTO.getState() == null ? State.CREATED : State.valueOf(TaskDTO.getState()))
                .build();
    }

    @Override
    public TaskDTO reverseConvert(Task Task) throws CustomException {
        return TaskDTO.builder()
                .id(Task.getId())
                .task(Task.getTask())
                .kind(Task.getKind())
                .project(Task.getProject())
                .state(Task.getState() == null ? State.CREATED.name() : Task.getState().name())
                .created(Task.getCreated())
                .updated(Task.getUpdated())
                .build();
    }

}