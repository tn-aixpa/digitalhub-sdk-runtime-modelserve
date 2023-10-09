package it.smartcommunitylabdhub.core.controllers.v1.context;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
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
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Operation;
import it.smartcommunitylabdhub.core.annotations.ApiVersion;
import it.smartcommunitylabdhub.core.annotations.ValidateField;
import it.smartcommunitylabdhub.core.models.entities.workflow.WorkflowDTO;
import it.smartcommunitylabdhub.core.services.context.interfaces.WorkflowContextService;
import jakarta.validation.Valid;

@RestController
@ApiVersion("v1")
@Validated
public class WorkflowContextController implements ContextController {

        @Autowired
        WorkflowContextService workflowContextService;

        @Operation(summary = "Create an workflow in a project context",
                        description = "First check if project exist and then create the workflow for the project (context)")
        @PostMapping(value = "/workflows", consumes = {MediaType.APPLICATION_JSON_VALUE,
                        "application/x-yaml"}, produces = "application/json; charset=UTF-8")
        public ResponseEntity<WorkflowDTO> createWorkflow(
                        @ValidateField @PathVariable String project,
                        @Valid @RequestBody WorkflowDTO workflowDTO) {
                return ResponseEntity.ok(
                                this.workflowContextService.createWorkflow(project, workflowDTO));
        }

        @Operation(summary = "Retrive only the latest version of all workflow",
                        description = "First check if project exist and then return a list of the latest version of each workflow related to a project)")
        @GetMapping(path = "/workflows", produces = "application/json; charset=UTF-8")
        public ResponseEntity<List<WorkflowDTO>> getLatestWorkflows(
                        @ValidateField @PathVariable String project,
                        Pageable pageable) {

                return ResponseEntity.ok(this.workflowContextService
                                .getLatestByProjectName(project, pageable));
        }

        @Operation(summary = "Retrieve all versions of the workflow sort by creation",
                        description = "First check if project exist and then return a list of all version of the workflow sort by creation)")
        @GetMapping(path = "/workflows/{name}", produces = "application/json; charset=UTF-8")
        public ResponseEntity<List<WorkflowDTO>> getAllWorkflows(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name,
                        Pageable pageable) {

                return ResponseEntity.ok(this.workflowContextService
                                .getByProjectNameAndWorkflowName(project, name, pageable));

        }

        @Operation(summary = "Retrive a specific workflow version given the workflow uuid",
                        description = "First check if project exist and then return a specific version of the workflow identified by the uuid)")
        @GetMapping(path = "/workflows/{name}/{uuid}", produces = "application/json; charset=UTF-8")
        public ResponseEntity<WorkflowDTO> getWorkflowByUuid(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name,
                        @ValidateField @PathVariable String uuid) {

                return ResponseEntity.ok(this.workflowContextService
                                .getByProjectAndWorkflowAndUuid(project, name, uuid));

        }

        @Operation(summary = "Retrive the latest version of an workflow",
                        description = "First check if project exist and then return the latest version of an workflow)")
        @GetMapping(path = "/workflows/{name}/latest", produces = "application/json; charset=UTF-8")
        public ResponseEntity<WorkflowDTO> getLatestWorkflowByName(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name) {

                return ResponseEntity.ok(this.workflowContextService
                                .getLatestByProjectNameAndWorkflowName(project, name));
        }

        @Operation(summary = "Create an  or update an workflow in a project context",
                        description = "First check if project exist, if workflow exist update one otherwise create a new version of the workflow")
        @PostMapping(value = "/workflows/{name}", consumes = {MediaType.APPLICATION_JSON_VALUE,
                        "application/x-yaml"}, produces = "application/json; charset=UTF-8")
        public ResponseEntity<WorkflowDTO> createOrUpdateWorkflow(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name,
                        @Valid @RequestBody WorkflowDTO workflowDTO) {
                return ResponseEntity
                                .ok(this.workflowContextService.createOrUpdateWorkflow(project,
                                                name, workflowDTO));
        }

        @Operation(summary = "Update if exist an workflow in a project context",
                        description = "First check if project exist, if workflow exist update.")
        @PutMapping(value = "/workflows/{name}/{uuid}",
                        consumes = {MediaType.APPLICATION_JSON_VALUE,
                                        "application/x-yaml"},
                        produces = "application/json; charset=UTF-8")
        public ResponseEntity<WorkflowDTO> updateUpdateWorkflow(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name,
                        @ValidateField @PathVariable String uuid,
                        @Valid @RequestBody WorkflowDTO workflowDTO) {
                return ResponseEntity.ok(this.workflowContextService.updateWorkflow(project, name,
                                uuid, workflowDTO));
        }

        @Operation(summary = "Delete a specific workflow version",
                        description = "First check if project exist, then delete a specific workflow version")
        @DeleteMapping(path = "/workflows/{name}/{uuid}")
        public ResponseEntity<Boolean> deleteSpecificWorkflowVersion(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name,
                        @ValidateField @PathVariable String uuid) {
                return ResponseEntity
                                .ok(this.workflowContextService.deleteSpecificWorkflowVersion(
                                                project, name, uuid));
        }

        @Operation(summary = "Delete all version of an workflow",
                        description = "First check if project exist, then delete a specific workflow version")
        @DeleteMapping(path = "/workflows/{name}")
        public ResponseEntity<Boolean> deleteWorkflow(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name) {
                return ResponseEntity.ok(this.workflowContextService
                                .deleteAllWorkflowVersions(project, name));
        }
}
