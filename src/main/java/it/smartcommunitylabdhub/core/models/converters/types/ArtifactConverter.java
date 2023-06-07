package it.smartcommunitylabdhub.core.models.converters.types;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.entities.Artifact;
import it.smartcommunitylabdhub.core.models.enums.State;

@Component
public class ArtifactConverter implements Converter<ArtifactDTO, Artifact> {

    @Override
    public Artifact convert(ArtifactDTO artifactDTO) throws CustomException {
        return Artifact.builder()
                .id(artifactDTO.getId())
                .name(artifactDTO.getName())
                .kind(artifactDTO.getKind())
                .project(artifactDTO.getProject())
                .embedded(artifactDTO.getEmbedded())
                .state(artifactDTO.getState() == null ? State.CREATED : State.valueOf(artifactDTO.getState()))
                .build();
    }

    @Override
    public ArtifactDTO reverseConvert(Artifact artifact) throws CustomException {
        return ArtifactDTO.builder()
                .id(artifact.getId())
                .name(artifact.getName())
                .kind(artifact.getKind())
                .project(artifact.getProject())
                .embedded(artifact.getEmbedded())
                .state(artifact.getState() == null ? State.CREATED.name() : artifact.getState().name())
                .created(artifact.getCreated())
                .updated(artifact.getUpdated())
                .build();
    }

}