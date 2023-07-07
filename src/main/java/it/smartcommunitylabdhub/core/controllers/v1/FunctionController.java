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

import it.smartcommunitylabdhub.core.annotations.ApiVersion;
import it.smartcommunitylabdhub.core.annotations.ValidateField;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.dtos.RunDTO;
import it.smartcommunitylabdhub.core.services.interfaces.FunctionService;
import jakarta.validation.Valid;

@RestController
@RequestMapping("/functions")
@ApiVersion("v1")
@Validated
public class FunctionController {

    private final FunctionService functionService;

    public FunctionController(FunctionService functionService) {
        this.functionService = functionService;
    }

    @GetMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<FunctionDTO>> getFunctions(Pageable pageable) {
        return ResponseEntity.ok(this.functionService.getFunctions(pageable));
    }

    @PostMapping(value = "", consumes = { MediaType.APPLICATION_JSON_VALUE,
            "application/x-yaml" }, produces = "application/json; charset=UTF-8")
    public ResponseEntity<FunctionDTO> createFunction(@Valid @RequestBody FunctionDTO functionDTO) {
        return ResponseEntity.ok(this.functionService.createFunction(functionDTO));
    }

    @GetMapping(path = "/{uuid}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<FunctionDTO> getFunction(
            @ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.functionService.getFunction(uuid));
    }

    @PutMapping(path = "/{uuid}", consumes = { MediaType.APPLICATION_JSON_VALUE,
            "application/x-yaml" }, produces = "application/json; charset=UTF-8")
    public ResponseEntity<FunctionDTO> updateFunction(@Valid @RequestBody FunctionDTO functionDTO,
            @ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.functionService.updateFunction(functionDTO, uuid));
    }

    @DeleteMapping(path = "/{uuid}")
    public ResponseEntity<Boolean> deleteFunction(@ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.functionService.deleteFunction(uuid));
    }

    @GetMapping(path = "/{uuid}/runs", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<RunDTO>> functionRuns(@ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.functionService.getFunctionRuns(uuid));
    }
}
