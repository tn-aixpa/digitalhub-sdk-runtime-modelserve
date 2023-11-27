package it.smartcommunitylabdhub.core.services.interfaces;

import it.smartcommunitylabdhub.core.models.entities.artifact.ArtifactDTO;
import org.springframework.data.domain.Pageable;

import java.util.List;

public interface ArtifactService {
    List<ArtifactDTO> getArtifacts(Pageable pageable);

    ArtifactDTO createArtifact(ArtifactDTO artifactDTO);

    ArtifactDTO getArtifact(String uuid);

    ArtifactDTO updateArtifact(ArtifactDTO artifactDTO, String uuid);

    boolean deleteArtifact(String uuid);

}
