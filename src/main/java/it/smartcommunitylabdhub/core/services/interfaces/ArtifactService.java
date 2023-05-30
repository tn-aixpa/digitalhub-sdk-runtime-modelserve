package it.smartcommunitylabdhub.core.services.interfaces;

import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.entities.Artifact;

import java.util.List;

import org.springframework.data.domain.Pageable;

public interface ArtifactService {
    List<ArtifactDTO> getArtifacts(Pageable pageable);

    ArtifactDTO createArtifact(ArtifactDTO artifactDTO);

    ArtifactDTO getArtifact(String uuid);

    ArtifactDTO updateArtifact(ArtifactDTO artifactDTO, String uuid);

    boolean deleteArtifact(String uuid);

    // Context artifact method
    List<ArtifactDTO> getByProjectNameAndArtifactName(
            String projectName, String artifactName, Pageable pageable);

    ArtifactDTO getLatestByProjectNameAndArtifactName(
            String projectName, String artifactName);

    ArtifactDTO getLatestByProjectNameAndArtifactNameAndArtifactUuid(
            String projectName, String artifactName, String uuid);

}
