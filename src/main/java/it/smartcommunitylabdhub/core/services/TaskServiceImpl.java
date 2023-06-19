package it.smartcommunitylabdhub.core.services;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.builders.dtos.TaskDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.entities.TaskEntityBuilder;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
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
                    .map(task -> new TaskDTOBuilder(task).build())
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
        return taskRepository.findById(uuid).map(task -> new TaskDTOBuilder(task).build())
                .orElseThrow(() -> new CoreException(
                        "TaskNotFound",
                        "The Task you are searching for does not exist.",
                        HttpStatus.NOT_FOUND));
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
    public TaskDTO createTask(@Valid TaskDTO taskDTO) {

        // // 1. get function get if exist otherwise throw exeception.
        // return
        // functionRepository.findLatestFunctionByProjectAndId(taskDTO.getProject(),
        // uuidOrName)
        // .or(() -> functionRepository.findLatestFunctionByProjectAndName(
        // taskDTO.getProject(), uuidOrName))
        // .map(function -> {

        // // 2. store task and create run object
        // Task task = new TaskEntityBuilder(taskDTO).build();
        // taskRepository.save(task);

        // // 3. produce a run object and store it
        // Run run = new RunEntityBuilder(
        // RunDTO.builder()
        // .type(function.getKind())
        // .taskId(task.getId())
        // .project(function.getProject())
        // .name(taskDTO.getName() + "@task:" + task.getId())
        // .body(Map.of())
        // .build())
        // .build();
        // this.runRepository.save(run);

        // // 4. produce event with the runDTO object
        // RunDTO runDTO = new RunDTOBuilder(run).build();
        // JobMessage jobMessage = new JobMessage(runDTO, new
        // TaskDTOBuilder(task).build());
        // messageDispatcher.dispatch(jobMessage);

        // // 5. return the runDTO object to client
        // return runDTO;

        // }).orElseThrow(() -> new CoreException(
        // "FunctionNotFound",
        // "The function you are searching for does not exist.",
        // HttpStatus.NOT_FOUND));

        return null;
    }
}
