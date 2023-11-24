package it.smartcommunitylabdhub.core.services.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;
import it.smartcommunitylabdhub.core.models.entities.artifact.Artifact;

public interface ArtifactService {
        List<Artifact> getArtifacts(Pageable pageable);

        Artifact createArtifact(Artifact artifactDTO);

        Artifact getArtifact(String uuid);

        Artifact updateArtifact(Artifact artifactDTO, String uuid);

        boolean deleteArtifact(String uuid);

}
