package it.smartcommunitylabdhub.core.controllers.v1.context;

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
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Operation;
import it.smartcommunitylabdhub.core.annotations.ApiVersion;
import it.smartcommunitylabdhub.core.models.dtos.DataItemDTO;
import it.smartcommunitylabdhub.core.services.context.interfaces.DataItemContextService;

@RestController
@ApiVersion("v1")
public class DataItemContextController extends ContextController {

    private final DataItemContextService dataItemContextService;

    public DataItemContextController(DataItemContextService dataItemContextService) {
        this.dataItemContextService = dataItemContextService;
    }

    @Operation(summary = "Create an dataItem in a project context", description = "First check if project exist and then create the dataItem for the project (context)")
    @PostMapping(value = "/dataItems", consumes = { MediaType.APPLICATION_JSON_VALUE, "application/x-yaml" })
    public ResponseEntity<DataItemDTO> createDataItem(
            @PathVariable String project,
            @RequestBody DataItemDTO dataItemDTO) {
        return ResponseEntity.ok(this.dataItemContextService.createDataItem(project, dataItemDTO));
    }

    @Operation(summary = "Retrive only the latest version of all dataItem", description = "First check if project exist and then return a list of the latest version of each dataItem related to a project)")
    @GetMapping(path = "/dataItems", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<DataItemDTO>> getLatestDataItems(
            @PathVariable String project,
            Pageable pageable) {

        return ResponseEntity.ok(this.dataItemContextService
                .getLatestByProjectName(project, pageable));
    }

    @Operation(summary = "Retrieve all versions of the dataItem sort by creation", description = "First check if project exist and then return a list of all version of the dataItem sort by creation)")
    @GetMapping(path = "/dataItems/{name}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<DataItemDTO>> getAllDataItems(
            @PathVariable String project,
            @PathVariable String name,
            Pageable pageable) {

        return ResponseEntity.ok(this.dataItemContextService
                .getByProjectNameAndDataItemName(project, name, pageable));

    }

    @Operation(summary = "Retrive a specific dataItem version given the dataItem uuid", description = "First check if project exist and then return a specific version of the dataItem identified by the uuid)")
    @GetMapping(path = "/dataItems/{name}/{uuid}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<DataItemDTO> getDataItemByUuid(
            @PathVariable String project,
            @PathVariable String name,
            @PathVariable String uuid) {

        return ResponseEntity.ok(this.dataItemContextService
                .getByProjectAndDataItemAndUuid(project, name, uuid));

    }

    @Operation(summary = "Retrive the latest version of an dataItem", description = "First check if project exist and then return the latest version of an dataItem)")
    @GetMapping(path = "/dataItems/{name}/latest", produces = "application/json; charset=UTF-8")
    public ResponseEntity<DataItemDTO> getLatestDataItemByName(
            @PathVariable String project,
            @PathVariable String name) {

        return ResponseEntity.ok(this.dataItemContextService
                .getLatestByProjectNameAndDataItemName(project, name));
    }

    @Operation(summary = "Create an  or update an dataItem in a project context", description = "First check if project exist, if dataItem exist update one otherwise create a new version of the dataItem")
    @PostMapping(value = "/dataItems/{name}", consumes = { MediaType.APPLICATION_JSON_VALUE, "application/x-yaml" })
    public ResponseEntity<DataItemDTO> createOrUpdateDataItem(
            @PathVariable String project,
            @PathVariable String name,
            @RequestBody DataItemDTO dataItemDTO) {
        return ResponseEntity.ok(this.dataItemContextService.createOrUpdateDataItem(project, name, dataItemDTO));
    }

    @Operation(summary = "Update if exist an dataItem in a project context", description = "First check if project exist, if dataItem exist update.")
    @PutMapping(value = "/dataItems/{name}/{uuid}", consumes = { MediaType.APPLICATION_JSON_VALUE,
            "application/x-yaml" })
    public ResponseEntity<DataItemDTO> updateUpdateDataItem(
            @PathVariable String project,
            @PathVariable String name,
            @PathVariable String uuid,
            @RequestBody DataItemDTO dataItemDTO) {
        return ResponseEntity.ok(this.dataItemContextService.updateDataItem(project, name, uuid, dataItemDTO));
    }

    @Operation(summary = "Delete a specific dataItem version", description = "First check if project exist, then delete a specific dataItem version")
    @DeleteMapping(path = "/dataItems/{name}/{uuid}")
    public ResponseEntity<Boolean> deleteSpecificDataItemVersion(
            @PathVariable String project,
            @PathVariable String name,
            @PathVariable String uuid) {
        return ResponseEntity.ok(this.dataItemContextService.deleteSpecificDataItemVersion(project, name, uuid));
    }

    @Operation(summary = "Delete all version of an dataItem", description = "First check if project exist, then delete a specific dataItem version")
    @DeleteMapping(path = "/dataItems/{name}")
    public ResponseEntity<Boolean> deleteDataItem(
            @PathVariable String project,
            @PathVariable String name) {
        return ResponseEntity.ok(this.dataItemContextService.deleteAllDataItemVersions(project, name));
    }
}
