package it.smartcommunitylabdhub.core.services.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;

import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;

public interface TaskService {

    List<TaskDTO> getTasks(Pageable pageable);

    TaskDTO getTask(String uuid);

    boolean deleteTask(String uuid);

    TaskDTO createTask(TaskDTO TaskDTO);

}
