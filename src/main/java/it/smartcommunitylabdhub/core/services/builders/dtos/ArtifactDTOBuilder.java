package it.smartcommunitylabdhub.core.services.builders.dtos;

import java.util.Optional;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.entities.Artifact;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.services.factory.EntityFactory;

public class ArtifactDTOBuilder {

        private CommandFactory commandFactory;
        private Artifact artifact;
        private boolean embeddable;

        public ArtifactDTOBuilder(
                        CommandFactory commandFactory,
                        Artifact artifact,
                        boolean embeddable) {
                this.artifact = artifact;
                this.embeddable = embeddable;
                this.commandFactory = commandFactory;
        }

        public ArtifactDTO build() {
                return EntityFactory.create(ArtifactDTO::new, artifact, builder -> {
                        builder
                                        .with(dto -> dto.setId(artifact.getId()))
                                        .with(dto -> dto.setKind(artifact.getKind()))
                                        .with(dto -> dto.setProject(artifact.getProject()))
                                        .with(dto -> dto.setName(artifact.getName()))

                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(artifact.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setSpec(ConversionUtils.reverse(
                                                                                                artifact.getSpec(),
                                                                                                commandFactory,
                                                                                                "cbor")));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(artifact.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setExtra(ConversionUtils.reverse(
                                                                                                artifact.getExtra(),
                                                                                                commandFactory,
                                                                                                "cbor")));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(artifact.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setCreated(artifact.getCreated()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(artifact.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setUpdated(artifact.getUpdated()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {
                                                Optional.ofNullable(artifact.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setEmbedded(artifact.getEmbedded()));
                                        })
                                        .withIfElse(embeddable, (dto, condition) -> {

                                                Optional.ofNullable(artifact.getEmbedded())
                                                                .filter(embedded -> !condition
                                                                                || (condition && embedded))
                                                                .ifPresent(embedded -> dto
                                                                                .setState(artifact.getState() == null
                                                                                                ? State.CREATED.name()
                                                                                                : artifact.getState()
                                                                                                                .name()));

                                        });

                });
        }
}