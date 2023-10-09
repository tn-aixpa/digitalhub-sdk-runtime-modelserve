package it.smartcommunitylabdhub.core.models.converters.types;

import org.springframework.stereotype.Component;

import it.smartcommunitylabdhub.core.components.fsm.enums.ArtifactState;
import it.smartcommunitylabdhub.core.exceptions.CustomException;
import it.smartcommunitylabdhub.core.models.converters.interfaces.Converter;
import it.smartcommunitylabdhub.core.models.entities.artifact.Artifact;
import it.smartcommunitylabdhub.core.models.entities.artifact.ArtifactDTO;

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
                .state(artifactDTO.getState() == null ? ArtifactState.CREATED
                        : ArtifactState.valueOf(artifactDTO.getState()))
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
                .state(artifact.getState() == null ? ArtifactState.CREATED.name()
                        : artifact.getState().name())
                .created(artifact.getCreated())
                .updated(artifact.getUpdated())
                .build();
    }

}
