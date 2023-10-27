package it.smartcommunitylabdhub.core.models.converters.types;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.entities.task.Task;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
import it.smartcommunitylabdhub.core.models.enums.State;
import org.springframework.stereotype.Component;

@Component
public class TaskConverter implements Converter<TaskDTO, Task> {

    @Override
    public Task convert(TaskDTO taskDTO) throws CustomException {
        return Task.builder()
                .id(taskDTO.getId())
                .kind(taskDTO.getKind())
                .project(taskDTO.getProject())
                .state(taskDTO.getState() == null ? State.CREATED
                        : State.valueOf(taskDTO.getState()))
                .build();
    }

    @Override
    public TaskDTO reverseConvert(Task task) throws CustomException {
        return TaskDTO.builder()
                .id(task.getId())
                .kind(task.getKind())
                .project(task.getProject())
                .state(task.getState() == null ? State.CREATED.name() : task.getState().name())
                .created(task.getCreated())
                .updated(task.getUpdated())
                .build();
    }

}
