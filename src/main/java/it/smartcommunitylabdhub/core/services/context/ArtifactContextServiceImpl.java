package it.smartcommunitylabdhub.core.services.context;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.builders.dtos.ArtifactDTOBuilder;
import it.smartcommunitylabdhub.core.models.builders.entities.ArtifactEntityBuilder;
import it.smartcommunitylabdhub.core.models.entities.artifact.Artifact;
import it.smartcommunitylabdhub.core.models.entities.artifact.ArtifactDTO;
import it.smartcommunitylabdhub.core.repositories.ArtifactRepository;
import it.smartcommunitylabdhub.core.services.context.interfaces.ArtifactContextService;
import jakarta.transaction.Transactional;

@Service
public class ArtifactContextServiceImpl extends ContextService implements ArtifactContextService {

    @Autowired
    ArtifactRepository artifactRepository;

    @Autowired
    ArtifactEntityBuilder artifactEntityBuilder;

    @Autowired
    ArtifactDTOBuilder artifactDTOBuilder;

    @Override
    public ArtifactDTO createArtifact(String projectName, ArtifactDTO artifactDTO) {
        try {
            // Check that project context is the same as the project passed to the
            // artifactDTO
            if (!projectName.equals(artifactDTO.getProject())) {
                throw new CustomException("Project Context and Artifact Project does not match",
                        null);
            }

            // Check project context
            checkContext(artifactDTO.getProject());

            // Check if artifact already exist if exist throw exception otherwise create a
            // new one
            Artifact artifact = (Artifact) Optional.ofNullable(artifactDTO.getId())
                    .flatMap(id -> artifactRepository.findById(id)
                            .map(a -> {
                                throw new CustomException(
                                        "The project already contains an artifact with the specified UUID.",
                                        null);
                            }))
                    .orElseGet(() -> {
                        // Build an artifact and store it in the database
                        Artifact newArtifact = artifactEntityBuilder.build(artifactDTO);
                        return artifactRepository.save(newArtifact);
                    });

            // Return artifact DTO
            return artifactDTOBuilder.build(artifact, false);

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<ArtifactDTO> getLatestByProjectName(String projectName, Pageable pageable) {
        try {
            checkContext(projectName);

            Page<Artifact> artifactPage = this.artifactRepository
                    .findAllLatestArtifactsByProject(projectName,
                            pageable);
            return artifactPage.getContent()
                    .stream()
                    .map((artifact) -> {
                        return artifactDTOBuilder.build(artifact, false);
                    }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<ArtifactDTO> getByProjectNameAndArtifactName(String projectName,
            String artifactName,
            Pageable pageable) {
        try {
            checkContext(projectName);

            Page<Artifact> artifactPage = this.artifactRepository
                    .findAllByProjectAndNameOrderByCreatedDesc(projectName, artifactName,
                            pageable);
            return artifactPage.getContent()
                    .stream()
                    .map((artifact) -> {
                        return artifactDTOBuilder.build(artifact, false);
                    }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }

    }

    @Override
    public ArtifactDTO getByProjectAndArtifactAndUuid(String projectName, String artifactName,
            String uuid) {
        try {
            // Check project context
            checkContext(projectName);

            return this.artifactRepository
                    .findByProjectAndNameAndId(projectName, artifactName, uuid).map(
                            artifact -> artifactDTOBuilder.build(artifact, false))
                    .orElseThrow(
                            () -> new CustomException("The artifact does not exist.", null));

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public ArtifactDTO getLatestByProjectNameAndArtifactName(String projectName,
            String artifactName) {
        try {
            // Check project context
            checkContext(projectName);

            return this.artifactRepository
                    .findLatestArtifactByProjectAndName(projectName, artifactName).map(
                            artifact -> artifactDTOBuilder.build(artifact, false))
                    .orElseThrow(
                            () -> new CustomException("The artifact does not exist.", null));

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public ArtifactDTO createOrUpdateArtifact(String projectName, String artifactName,
            ArtifactDTO artifactDTO) {
        try {
            // Check that project context is the same as the project passed to the
            // artifactDTO
            if (!projectName.equals(artifactDTO.getProject())) {
                throw new CustomException("Project Context and Artifact Project does not match.",
                        null);
            }
            if (!artifactName.equals(artifactDTO.getName())) {
                throw new CustomException(
                        "Trying to create/update an artifact with name different from the one passed in the request.",
                        null);
            }

            // Check project context
            checkContext(artifactDTO.getProject());

            // Check if artifact already exist if exist throw exception otherwise create a
            // new one
            Artifact artifact = Optional.ofNullable(artifactDTO.getId())
                    .flatMap(id -> {
                        Optional<Artifact> optionalArtifact = artifactRepository.findById(id);
                        if (optionalArtifact.isPresent()) {
                            Artifact existingArtifact = optionalArtifact.get();

                            // Update the existing artifact version
                            final Artifact artifactUpdated =
                                    artifactEntityBuilder.update(existingArtifact,
                                            artifactDTO);
                            return Optional.of(this.artifactRepository.save(artifactUpdated));

                        } else {
                            // Build a new artifact and store it in the database
                            Artifact newArtifact = artifactEntityBuilder.build(artifactDTO);
                            return Optional.of(artifactRepository.save(newArtifact));
                        }
                    })
                    .orElseGet(() -> {
                        // Build a new artifact and store it in the database
                        Artifact newArtifact = artifactEntityBuilder.build(artifactDTO);
                        return artifactRepository.save(newArtifact);
                    });

            // Return artifact DTO
            return artifactDTOBuilder.build(artifact, false);

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public ArtifactDTO updateArtifact(String projectName, String artifactName, String uuid,
            ArtifactDTO artifactDTO) {

        try {
            // Check that project context is the same as the project passed to the
            // artifactDTO
            if (!projectName.equals(artifactDTO.getProject())) {
                throw new CustomException("Project Context and Artifact Project does not match",
                        null);
            }
            if (!uuid.equals(artifactDTO.getId())) {
                throw new CustomException(
                        "Trying to update an artifact with an ID different from the one passed in the request.",
                        null);
            }
            // Check project context
            checkContext(artifactDTO.getProject());

            Artifact artifact = this.artifactRepository.findById(artifactDTO.getId()).map(
                    a -> {
                        // Update the existing artifact version
                        return artifactEntityBuilder.update(a, artifactDTO);
                    })
                    .orElseThrow(
                            () -> new CustomException("The artifact does not exist.", null));

            // Return artifact DTO
            return artifactDTOBuilder.build(artifact, false);

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional
    public Boolean deleteSpecificArtifactVersion(String projectName, String artifactName,
            String uuid) {
        try {
            if (this.artifactRepository.existsByProjectAndNameAndId(projectName, artifactName,
                    uuid)) {
                this.artifactRepository.deleteByProjectAndNameAndId(projectName, artifactName,
                        uuid);
                return true;
            }
            throw new CoreException(
                    "ArtifactNotFound",
                    "The artifact you are trying to delete does not exist.",
                    HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            throw new CoreException(
                    "InternalServerError",
                    "cannot delete artifact",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional
    public Boolean deleteAllArtifactVersions(String projectName, String artifactName) {
        try {
            if (artifactRepository.existsByProjectAndName(projectName, artifactName)) {
                this.artifactRepository.deleteByProjectAndName(projectName, artifactName);
                return true;
            }
            throw new CoreException(
                    "ArtifactNotFound",
                    "The artifacts you are trying to delete does not exist.",
                    HttpStatus.NOT_FOUND);
        } catch (Exception e) {
            throw new CoreException(
                    "InternalServerError",
                    "cannot delete artifact",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
