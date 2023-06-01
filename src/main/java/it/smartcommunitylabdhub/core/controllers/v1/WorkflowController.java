package it.smartcommunitylabdhub.core.controllers.v1;

import java.util.List;
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

import it.smartcommunitylabdhub.core.annotations.ApiVersion;
import it.smartcommunitylabdhub.core.annotations.ValidateField;
import it.smartcommunitylabdhub.core.models.dtos.WorkflowDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.services.interfaces.WorkflowService;

@RestController
@RequestMapping("/workflows")
@ApiVersion("v1")
public class WorkflowController {

    private final WorkflowService workflowService;

    public WorkflowController(WorkflowService workflowService) {
        this.workflowService = workflowService;
    }

    @GetMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<WorkflowDTO>> getWorkflows(Pageable pageable) {
        return ResponseEntity.ok(this.workflowService.getWorkflows(pageable));
    }

    @PostMapping(value = "", consumes = { MediaType.APPLICATION_JSON_VALUE, "application/x-yaml" })
    public ResponseEntity<WorkflowDTO> createWorkflow(@RequestBody WorkflowDTO workflowDTO) {
        return ResponseEntity.ok(this.workflowService.createWorkflow(workflowDTO));
    }

    @GetMapping(path = "/{uuid}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<WorkflowDTO> getWorkflow(
            @ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.workflowService.getWorkflow(uuid));
    }

    @PutMapping(path = "/{uuid}", consumes = { MediaType.APPLICATION_JSON_VALUE,
            "application/x-yaml" }, produces = "application/json")
    public ResponseEntity<WorkflowDTO> updateWorkflow(@RequestBody WorkflowDTO workflowDTO,
            @ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.workflowService.updateWorkflow(workflowDTO, uuid));
    }

    @DeleteMapping(path = "/{uuid}")
    public ResponseEntity<Boolean> deleteWorkflow(@ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.workflowService.deleteWorkflow(uuid));
    }

    @GetMapping(path = "/{uuid}/runs", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<RunDTO>> workflowRuns(@ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.workflowService.getWorkflowRuns(uuid));
    }

}
