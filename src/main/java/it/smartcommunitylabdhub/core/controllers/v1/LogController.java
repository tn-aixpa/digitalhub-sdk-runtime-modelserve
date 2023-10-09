package it.smartcommunitylabdhub.core.controllers.v1;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Operation;
import it.smartcommunitylabdhub.core.annotations.ApiVersion;
import it.smartcommunitylabdhub.core.annotations.ValidateField;
import it.smartcommunitylabdhub.core.models.entities.log.LogDTO;
import it.smartcommunitylabdhub.core.services.interfaces.LogService;

@RestController
@RequestMapping("/logs")
@ApiVersion("v1")
public class LogController {

    @Autowired
    LogService logService;

    @Operation(summary = "Get specific log", description = "Given a uuid return a specific log")
    @GetMapping(path = "/{uuid}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<LogDTO> getLog(
            @ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.logService.getLog(uuid));
    }

    @Operation(summary = "Log list", description = "Return the log list")
    @GetMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<LogDTO>> getLogs(Pageable pageable) {
        return ResponseEntity.ok(this.logService.getLogs(pageable));
    }

    @Operation(summary = "Delete a log", description = "Delete a specific log")
    @DeleteMapping(path = "/{uuid}")
    public ResponseEntity<Boolean> deleteLog(
            @ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.logService.deleteLog(uuid));
    }
}
