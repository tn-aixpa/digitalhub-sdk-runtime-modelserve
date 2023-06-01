package it.smartcommunitylabdhub.core.services.context.interfaces;

import java.util.List;

import org.springframework.data.domain.Pageable;

import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;

public interface ArtifactContextService {

        ArtifactDTO createArtifact(String projectName, ArtifactDTO artifactDTO);

        List<ArtifactDTO> getByProjectNameAndArtifactName(
                        String projectName, String artifactName, Pageable pageable);

        List<ArtifactDTO> getLatestByProjectName(
                        String projectName, Pageable pageable);

        ArtifactDTO getByProjectAndArtifactAndUuid(
                        String projectName, String artifactName, String uuid);

        ArtifactDTO getLatestByProjectNameAndArtifactName(
                        String projectName, String artifactName);

        ArtifactDTO createOrUpdateArtifact(String projectName, String artifactName, ArtifactDTO artifactDTO);

        ArtifactDTO updateArtifact(String projectName, String artifactName, String uuid, ArtifactDTO artifactDTO);
}
