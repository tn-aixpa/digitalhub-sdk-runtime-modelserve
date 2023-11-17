package it.smartcommunitylabdhub.core.services.context.interfaces;

import it.smartcommunitylabdhub.core.models.entities.artifact.ArtifactDTO;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface ArtifactContextService {

    ArtifactDTO createArtifact(String projectName, ArtifactDTO artifactDTO);

    Page<ArtifactDTO> getByProjectNameAndArtifactName(
            String projectName, String artifactName, Pageable pageable);

    Page<ArtifactDTO> getLatestByProjectName(
            String projectName, Pageable pageable);

    ArtifactDTO getByProjectAndArtifactAndUuid(
            String projectName, String artifactName, String uuid);

    ArtifactDTO getLatestByProjectNameAndArtifactName(
            String projectName, String artifactName);

    ArtifactDTO createOrUpdateArtifact(String projectName, String artifactName,
                                       ArtifactDTO artifactDTO);

    ArtifactDTO updateArtifact(String projectName, String artifactName, String uuid,
                               ArtifactDTO artifactDTO);

    Boolean deleteSpecificArtifactVersion(String projectName, String artifactName, String uuid);

    Boolean deleteAllArtifactVersions(String projectName, String artifactName);
}
