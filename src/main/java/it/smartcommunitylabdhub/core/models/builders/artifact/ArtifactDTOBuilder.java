package it.smartcommunitylabdhub.core.models.builders.artifact;

import it.smartcommunitylabdhub.core.components.fsm.enums.ArtifactState;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecRegistry;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.converters.types.MetadataConverter;
import it.smartcommunitylabdhub.core.models.entities.artifact.Artifact;
import it.smartcommunitylabdhub.core.models.entities.artifact.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.entities.artifact.metadata.ArtifactMetadata;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.Optional;

@Component
public class ArtifactDTOBuilder {

    @Autowired
    SpecRegistry<? extends Spec> specRegistry;

    @Autowired
    MetadataConverter<ArtifactMetadata> metadataConverter;

    public ArtifactDTO build(Artifact artifact, Boolean embeddable) {

        // Retrieve spec
        Map<String, Object> spec = ConversionUtils.reverse(artifact.getSpec(), "cbor");

        // Find function spec
        Spec artifactSpec = specRegistry.createSpec(
                artifact.getKind(),
                SpecEntity.ARTIFACT,
                spec);

        // Add base spec to the one stored in db
        spec.putAll(artifactSpec.toMap());

        return EntityFactory.create(ArtifactDTO::new, artifact, builder -> builder
                .with(dto -> dto.setId(artifact.getId()))
                .with(dto -> dto.setKind(artifact.getKind()))
                .with(dto -> dto.setProject(artifact.getProject()))
                .with(dto -> dto.setName(artifact.getName()))
                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(artifact.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto.setMetadata(Optional
                                .ofNullable(metadataConverter
                                        .reverseByClass(artifact
                                                        .getMetadata(),
                                                ArtifactMetadata.class))
                                .orElseGet(ArtifactMetadata::new))))
                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(artifact.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto
                                .setSpec(spec)))
                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(artifact.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto
                                .setExtra(ConversionUtils.reverse(
                                        artifact.getExtra(),
                                        "cbor"))))
                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(artifact.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto
                                .setCreated(artifact.getCreated())))
                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(artifact.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto
                                .setUpdated(artifact.getUpdated())))
                .withIfElse(embeddable, (dto, condition) -> Optional
                        .ofNullable(artifact.getEmbedded())
                        .filter(embedded -> !condition
                                || (condition && embedded))
                        .ifPresent(embedded -> dto
                                .setEmbedded(artifact
                                        .getEmbedded())))
                .withIfElse(embeddable, (dto, condition) ->

                        Optional.ofNullable(artifact.getEmbedded())
                                .filter(embedded -> !condition
                                        || (condition && embedded))
                                .ifPresent(embedded -> dto
                                        .setState(artifact
                                                .getState() == null
                                                ? ArtifactState.CREATED
                                                .name()
                                                : artifact.getState()
                                                .name()))

                )

        );
    }
}
