package it.smartcommunitylabdhub.core.controllers.v1;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Pageable;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Operation;
import it.smartcommunitylabdhub.core.annotations.ApiVersion;
import it.smartcommunitylabdhub.core.annotations.ValidateField;
import it.smartcommunitylabdhub.core.models.entities.task.TaskDTO;
import it.smartcommunitylabdhub.core.services.interfaces.TaskService;
import jakarta.validation.Valid;

@RestController
@RequestMapping("/tasks")
@ApiVersion("v1")
public class TaskController {

    @Autowired
    TaskService taskService;

    @Operation(summary = "Get specific task", description = "Given a uuid return a specific task")
    @GetMapping(path = "/{uuid}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<TaskDTO> getTask(
            @ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.taskService.getTask(uuid));
    }

    @Operation(summary = "List of tasks", description = "Return the list of all tasks")
    @GetMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<TaskDTO>> getTasks(Pageable pageable) {
        return ResponseEntity.ok(this.taskService.getTasks(pageable));
    }

    @Operation(summary = "Create a task", description = "Create and return a new task")
    @PostMapping(path = "", consumes = {MediaType.APPLICATION_JSON_VALUE,
            "application/x-yaml"}, produces = "application/json; charset=UTF-8")
    public ResponseEntity<TaskDTO> createTask(@Valid @RequestBody TaskDTO taskDTO) {
        return ResponseEntity.ok(this.taskService.createTask(taskDTO));
    }

    @Operation(summary = "Update a task", description = "Update and return a task")
    @PutMapping(path = "/{uuid}", consumes = {MediaType.APPLICATION_JSON_VALUE,
            "application/x-yaml"}, produces = "application/json; charset=UTF-8")
    public ResponseEntity<TaskDTO> updateTask(@Valid @RequestBody TaskDTO functionDTO,
            @ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.taskService.updateTask(functionDTO, uuid));
    }

    @Operation(summary = "Delete a task", description = "Delete a specific task")
    @DeleteMapping(path = "/{uuid}")
    public ResponseEntity<Boolean> deleteTask(
            @ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.taskService.deleteTask(uuid));
    }
}
