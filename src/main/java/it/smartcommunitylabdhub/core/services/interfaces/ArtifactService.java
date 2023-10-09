package it.smartcommunitylabdhub.core.services.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;
import it.smartcommunitylabdhub.core.models.entities.artifact.ArtifactDTO;

public interface ArtifactService {
        List<ArtifactDTO> getArtifacts(Pageable pageable);

        ArtifactDTO createArtifact(ArtifactDTO artifactDTO);

        ArtifactDTO getArtifact(String uuid);

        ArtifactDTO updateArtifact(ArtifactDTO artifactDTO, String uuid);

        boolean deleteArtifact(String uuid);

}
