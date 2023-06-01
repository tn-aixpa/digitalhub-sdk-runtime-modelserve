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
import it.smartcommunitylabdhub.core.models.dtos.DataItemDTO;
import it.smartcommunitylabdhub.core.services.interfaces.DataItemService;

@RestController
@RequestMapping("/dataitems")
@ApiVersion("v1")
public class DataItemController {

    private final DataItemService artifactService;

    public DataItemController(DataItemService artifactService) {
        this.artifactService = artifactService;
    }

    @GetMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<DataItemDTO>> getDataItems(Pageable pageable) {
        return ResponseEntity.ok(this.artifactService.getDataItems(pageable));
    }

    @PostMapping(value = "", consumes = { MediaType.APPLICATION_JSON_VALUE, "application/x-yaml" })
    public ResponseEntity<DataItemDTO> createDataItem(@RequestBody DataItemDTO artifactDTO) {
        return ResponseEntity.ok(this.artifactService.createDataItem(artifactDTO));
    }

    @GetMapping(path = "/{uuid}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<DataItemDTO> getDataItem(
            @ValidateField @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.artifactService.getDataItem(uuid));
    }

    @PutMapping(path = "/{uuid}", consumes = { MediaType.APPLICATION_JSON_VALUE,
            "application/x-yaml" }, produces = "application/json")
    public ResponseEntity<DataItemDTO> updateDataItem(@RequestBody DataItemDTO artifactDTO,
            @ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.artifactService.updateDataItem(artifactDTO, uuid));
    }

    @DeleteMapping(path = "/{uuid}")
    public ResponseEntity<Boolean> deleteDataItem(@ValidateField @PathVariable String uuid) {
        return ResponseEntity.ok(this.artifactService.deleteDataItem(uuid));
    }

}
