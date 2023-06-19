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
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.models.dtos.TaskDTO;
import it.smartcommunitylabdhub.core.services.interfaces.RunService;
import jakarta.validation.Valid;

@RestController
@RequestMapping("/runs")
@ApiVersion("v1")
public class RunController {

    private final RunService runService;

    public RunController(RunService runService) {
        this.runService = runService;
    }

    @GetMapping(path = "/{uuid}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<RunDTO> getRun(@ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.runService.getRun(uuid));
    }

    @GetMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<RunDTO>> getRuns(Pageable pageable) {
        return ResponseEntity.ok(this.runService.getRuns(pageable));
    }

    @PostMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<RunDTO> createRun(@Valid @RequestBody TaskDTO taskDTO) {
        return ResponseEntity.ok(this.runService.createRun(taskDTO));
    }

    @PostMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<RunDTO> executeRun(
            @ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.runService.executeRun(uuid));
    }

    @DeleteMapping(path = "/{uuid}")
    public ResponseEntity<Boolean> deleteRun(@ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.runService.deleteRun(uuid));
    }
}
