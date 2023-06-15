package it.smartcommunitylabdhub.core.services;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.models.entities.Task;
import it.smartcommunitylabdhub.core.repositories.TaskRepository;
import it.smartcommunitylabdhub.core.services.interfaces.TaskService;
import jakarta.validation.Valid;

@Service
public class TaskServiceImpl implements TaskService {

    private final TaskRepository taskRepository;

    public TaskServiceImpl(TaskRepository TaskRepository) {
        this.taskRepository = TaskRepository;
    }

    @Override
    public List<TaskDTO> getTasks(Pageable pageable) {
        try {
            Page<Task> TaskPage = this.taskRepository.findAll(pageable);
            return TaskPage.getContent().stream()
                    .map(Task -> (TaskDTO) ConversionUtils.reverse(Task, "task"))
                    .collect(Collectors.toList());

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public TaskDTO getTask(String uuid) {
        final Task Task = taskRepository.findById(uuid).orElse(null);
        if (Task == null) {
            throw new CoreException(
                    "TaskNotFound",
                    "The Task you are searching for does not exist.",
                    HttpStatus.NOT_FOUND);
        }

        try {
            return ConversionUtils.reverse(Task, "task");

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public boolean deleteTask(String uuid) {
        try {
            this.taskRepository.deleteById(uuid);
            return true;
        } catch (Exception e) {
            throw new CoreException(
                    "InternalServerError",
                    "cannot delete artifact",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public TaskDTO createTask(@Valid TaskDTO TaskDTO) {
        try {
            // Build a Task and store it on db

            final Task Task = ConversionUtils.convert(TaskDTO, "task");
            this.taskRepository.save(Task);

            return ConversionUtils.reverse(Task, "task");
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
