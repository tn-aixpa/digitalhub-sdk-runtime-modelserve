package it.smartcommunitylabdhub.core.controllers.v1.context;

import java.util.List;

import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylabdhub.core.annotations.ApiVersion;
import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.services.interfaces.ArtifactService;

@RestController
@ApiVersion("v1")
public class ArtifactContextController extends ContextController {

    private final ArtifactService artifactService;

    public ArtifactContextController(ArtifactService artifactService) {
        this.artifactService = artifactService;
    }

    @GetMapping(path = "/artifacts/{artifact}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<ArtifactDTO>> getArtifacts(
            @PathVariable String project,
            @PathVariable String artifact,
            Pageable pageable) {

        return ResponseEntity.ok(this.artifactService
                .getByProjectNameAndArtifactName(project, artifact, pageable));

    }

}
