package it.smartcommunitylabdhub.core.services.interfaces;

import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
import org.springframework.data.domain.Pageable;

import java.util.List;

public interface TaskService {

    List<TaskDTO> getTasks(Pageable pageable);

    TaskDTO getTask(String uuid);

    boolean deleteTask(String uuid);

    TaskDTO createTask(TaskDTO TaskDTO);

    TaskDTO updateTask(TaskDTO TaskDTO, String uuid);
}
