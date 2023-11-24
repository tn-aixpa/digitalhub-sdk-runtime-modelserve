package it.smartcommunitylabdhub.core.services.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;
import it.smartcommunitylabdhub.core.models.entities.task.Task;

public interface TaskService {

    List<Task> getTasks(Pageable pageable);

    Task getTask(String uuid);

    boolean deleteTask(String uuid);

    Task createTask(Task TaskDTO);

    Task updateTask(Task TaskDTO, String uuid);
}
