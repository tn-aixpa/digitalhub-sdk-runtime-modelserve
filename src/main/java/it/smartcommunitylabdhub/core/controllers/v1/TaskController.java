package it.smartcommunitylabdhub.core.controllers.v1;

import java.util.List;

import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylabdhub.core.annotations.ApiVersion;
import it.smartcommunitylabdhub.core.annotations.ValidateField;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.services.interfaces.TaskService;
import jakarta.validation.Valid;

@RestController
@RequestMapping("/tasks")
@ApiVersion("v1")
public class TaskController {

    private final TaskService taskService;

    public TaskController(TaskService taskService) {
        this.taskService = taskService;
    }

    @GetMapping(path = "/{uuid}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<TaskDTO> getTask(@ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.taskService.getTask(uuid));
    }

    @GetMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<TaskDTO>> getTasks(Pageable pageable) {
        return ResponseEntity.ok(this.taskService.getTasks(pageable));
    }

    @PostMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<TaskDTO> createTask(@Valid @RequestBody TaskDTO taskDTO) {
        return ResponseEntity.ok(this.taskService.createTask(taskDTO));
    }

    @DeleteMapping(path = "/{uuid}")
    public ResponseEntity<Boolean> deleteTask(
            @ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.taskService.deleteTask(uuid));
    }
}
