package it.smartcommunitylabdhub.core.controllers.v1;

import java.util.List;
import org.springframework.data.domain.Pageable;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
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
import it.smartcommunitylabdhub.core.models.dtos.WorkflowDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.services.interfaces.WorkflowService;
import jakarta.validation.Valid;

@RestController
@RequestMapping("/workflows")
@ApiVersion("v1")
@Validated
public class WorkflowController {

    private final WorkflowService workflowService;

    public WorkflowController(WorkflowService workflowService) {
        this.workflowService = workflowService;
    }

    @Operation(summary = "List workflows", description = "Return a list of all workflows")
    @GetMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<WorkflowDTO>> getWorkflows(Pageable pageable) {
        return ResponseEntity.ok(this.workflowService.getWorkflows(pageable));
    }

    @Operation(summary = "Create workflow", description = "Create an workflow and return")
    @PostMapping(value = "", consumes = { MediaType.APPLICATION_JSON_VALUE,
            "application/x-yaml" }, produces = "application/json; charset=UTF-8")
    public ResponseEntity<WorkflowDTO> createWorkflow(@Valid @RequestBody WorkflowDTO workflowDTO) {
        return ResponseEntity.ok(this.workflowService.createWorkflow(workflowDTO));
    }

    @Operation(summary = "Get an workflow by uuid", description = "Return an workflow")
    @GetMapping(path = "/{uuid}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<WorkflowDTO> getWorkflow(
            @ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.workflowService.getWorkflow(uuid));
    }

    @Operation(summary = "Update specific workflow", description = "Update and return the workflow")
    @PutMapping(path = "/{uuid}", consumes = { MediaType.APPLICATION_JSON_VALUE,
            "application/x-yaml" }, produces = "application/json; charset=UTF-8")
    public ResponseEntity<WorkflowDTO> updateWorkflow(@Valid @RequestBody WorkflowDTO workflowDTO,
            @ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.workflowService.updateWorkflow(workflowDTO, uuid));
    }

    @Operation(summary = "Delete an workflow", description = "Delete a specific workflow")
    @DeleteMapping(path = "/{uuid}")
    public ResponseEntity<Boolean> deleteWorkflow(@ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.workflowService.deleteWorkflow(uuid));
    }

    @GetMapping(path = "/{uuid}/runs", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<RunDTO>> workflowRuns(@ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.workflowService.getWorkflowRuns(uuid));
    }

}
