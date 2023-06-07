package it.smartcommunitylabdhub.core.services;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import it.smartcommunitylabdhub.core.exceptions.CoreException;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.entities.Artifact;
import it.smartcommunitylabdhub.core.repositories.ArtifactRepository;
import it.smartcommunitylabdhub.core.services.builders.dtos.ArtifactDTOBuilder;
import it.smartcommunitylabdhub.core.services.builders.entities.ArtifactEntityBuilder;
import it.smartcommunitylabdhub.core.services.interfaces.ArtifactService;

@Service
public class ArtifactServiceImpl implements ArtifactService {

    private final ArtifactRepository artifactRepository;
    private final CommandFactory commandFactory;

    public ArtifactServiceImpl(
            ArtifactRepository artifactRepository,
            CommandFactory commandFactory) {
        this.artifactRepository = artifactRepository;
        this.commandFactory = commandFactory;

    }

    @Override
    public List<ArtifactDTO> getArtifacts(Pageable pageable) {
        try {
            Page<Artifact> artifactPage = this.artifactRepository.findAll(pageable);
            return artifactPage.getContent().stream().map((artifact) -> {
                return new ArtifactDTOBuilder(commandFactory, artifact, false).build();
            }).collect(Collectors.toList());
        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }

    }

    @Override
    public ArtifactDTO createArtifact(ArtifactDTO artifactDTO) {
        try {
            // Build a artifact and store it on db
            final Artifact artifact = new ArtifactEntityBuilder(commandFactory, artifactDTO).build();
            this.artifactRepository.save(artifact);

            // Return artifact DTO
            return new ArtifactDTOBuilder(
                    commandFactory,
                    artifact, false).build();

        } catch (CustomException e) {
            throw new CoreException(
                    "InternalServerError",
                    e.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public ArtifactDTO getArtifact(String uuid) {
        return artifactRepository.findById(uuid)
                .map(artifact -> {
                    try {
                        return new ArtifactDTOBuilder(commandFactory, artifact, false).build();
                    } catch (CustomException e) {
                        throw new CoreException(
                                "InternalServerError",
                                e.getMessage(),
                                HttpStatus.INTERNAL_SERVER_ERROR);
                    }
                })
                .orElseThrow(() -> new CoreException(
                        "ArtifactNotFound",
                        "The artifact you are searching for does not exist.",
                        HttpStatus.NOT_FOUND));
    }

    @Override
    public ArtifactDTO updateArtifact(ArtifactDTO artifactDTO, String uuid) {
        if (!artifactDTO.getId().equals(uuid)) {
            throw new CoreException(
                    "ArtifactNotMatch",
                    "Trying to update an artifact with a UUID different from the one passed in the request.",
                    HttpStatus.NOT_FOUND);
        }

        return artifactRepository.findById(uuid)
                .map(artifact -> {
                    try {
                        ArtifactEntityBuilder artifactBuilder = new ArtifactEntityBuilder(commandFactory, artifactDTO);
                        Artifact artifactUpdated = artifactBuilder.update(artifact);
                        artifactRepository.save(artifactUpdated);
                        return new ArtifactDTOBuilder(commandFactory, artifactUpdated, false).build();
                    } catch (CustomException e) {
                        throw new CoreException(
                                "InternalServerError",
                                e.getMessage(),
                                HttpStatus.INTERNAL_SERVER_ERROR);
                    }
                })
                .orElseThrow(() -> new CoreException(
                        "ArtifactNotFound",
                        "The artifact you are searching for does not exist.",
                        HttpStatus.NOT_FOUND));
    }

    @Override
    public boolean deleteArtifact(String uuid) {
        try {
            if (this.artifactRepository.existsById(uuid)) {
                this.artifactRepository.deleteById(uuid);
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

}
