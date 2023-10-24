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
import it.smartcommunitylabdhub.core.annotations.validators.ValidateField;
import it.smartcommunitylabdhub.core.models.entities.function.FunctionDTO;
import it.smartcommunitylabdhub.core.services.context.interfaces.FunctionContextService;
import jakarta.validation.Valid;

@RestController
@ApiVersion("v1")
@Validated
public class FunctionContextController implements ContextController {

        @Autowired
        FunctionContextService functionContextService;

        @Operation(summary = "Create an function in a project context",
                        description = "First check if project exist and then create the function for the project (context)")
        @PostMapping(value = "/functions", consumes = {MediaType.APPLICATION_JSON_VALUE,
                        "application/x-yaml"}, produces = "application/json; charset=UTF-8")
        public ResponseEntity<FunctionDTO> createFunction(
                        @ValidateField @PathVariable String project,
                        @Valid @RequestBody FunctionDTO functionDTO) {
                return ResponseEntity.ok(
                                this.functionContextService.createFunction(project, functionDTO));
        }

        @Operation(summary = "Retrive only the latest version of all function",
                        description = "First check if project exist and then return a list of the latest version of each function related to a project)")
        @GetMapping(path = "/functions", produces = "application/json; charset=UTF-8")
        public ResponseEntity<List<FunctionDTO>> getLatestFunctions(
                        @ValidateField @PathVariable String project,
                        Pageable pageable) {

                return ResponseEntity.ok(this.functionContextService
                                .getLatestByProjectName(project, pageable));
        }

        @Operation(summary = "Retrieve all versions of the function sort by creation",
                        description = "First check if project exist and then return a list of all version of the function sort by creation)")
        @GetMapping(path = "/functions/{name}", produces = "application/json; charset=UTF-8")
        public ResponseEntity<List<FunctionDTO>> getAllFunctions(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name,
                        Pageable pageable) {

                return ResponseEntity.ok(this.functionContextService
                                .getByProjectNameAndFunctionName(project, name, pageable));

        }

        @Operation(summary = "Retrive a specific function version given the function uuid",
                        description = "First check if project exist and then return a specific version of the function identified by the uuid)")
        @GetMapping(path = "/functions/{name}/{uuid}", produces = "application/json; charset=UTF-8")
        public ResponseEntity<FunctionDTO> getFunctionByUuid(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name,
                        @ValidateField @PathVariable String uuid) {

                return ResponseEntity.ok(this.functionContextService
                                .getByProjectAndFunctionAndUuid(project, name, uuid));

        }

        @Operation(summary = "Retrive the latest version of an function",
                        description = "First check if project exist and then return the latest version of an function)")
        @GetMapping(path = "/functions/{name}/latest", produces = "application/json; charset=UTF-8")
        public ResponseEntity<FunctionDTO> getLatestFunctionByName(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name) {

                return ResponseEntity.ok(this.functionContextService
                                .getLatestByProjectNameAndFunctionName(project, name));
        }

        @Operation(summary = "Create an  or update an function in a project context",
                        description = "First check if project exist, if function exist update one otherwise create a new version of the function")
        @PostMapping(value = "/functions/{name}", consumes = {MediaType.APPLICATION_JSON_VALUE,
                        "application/x-yaml"}, produces = "application/json; charset=UTF-8")
        public ResponseEntity<FunctionDTO> createOrUpdateFunction(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name,
                        @Valid @RequestBody FunctionDTO functionDTO) {
                return ResponseEntity
                                .ok(this.functionContextService.createOrUpdateFunction(project,
                                                name, functionDTO));
        }

        @Operation(summary = "Update if exist an function in a project context",
                        description = "First check if project exist, if function exist update.")
        @PutMapping(value = "/functions/{name}/{uuid}",
                        consumes = {MediaType.APPLICATION_JSON_VALUE,
                                        "application/x-yaml"},
                        produces = "application/json; charset=UTF-8")
        public ResponseEntity<FunctionDTO> updateUpdateFunction(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name,
                        @ValidateField @PathVariable String uuid,
                        @Valid @RequestBody FunctionDTO functionDTO) {
                return ResponseEntity.ok(this.functionContextService.updateFunction(project, name,
                                uuid, functionDTO));
        }

        @Operation(summary = "Delete a specific function version",
                        description = "First check if project exist, then delete a specific function version")
        @DeleteMapping(path = "/functions/{name}/{uuid}")
        public ResponseEntity<Boolean> deleteSpecificFunctionVersion(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name,
                        @ValidateField @PathVariable String uuid) {
                return ResponseEntity
                                .ok(this.functionContextService.deleteSpecificFunctionVersion(
                                                project, name, uuid));
        }

        @Operation(summary = "Delete all version of an function",
                        description = "First check if project exist, then delete a specific function version")
        @DeleteMapping(path = "/functions/{name}")
        public ResponseEntity<Boolean> deleteFunction(
                        @ValidateField @PathVariable String project,
                        @ValidateField @PathVariable String name) {
                return ResponseEntity.ok(this.functionContextService
                                .deleteAllFunctionVersions(project, name));
        }

}
