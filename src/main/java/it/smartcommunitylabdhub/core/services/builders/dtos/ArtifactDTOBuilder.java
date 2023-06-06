package it.smartcommunitylabdhub.core.services.builders.dtos;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.entities.Artifact;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.services.factory.EntityFactory;

public class ArtifactDTOBuilder {

        private CommandFactory commandFactory;
        private Artifact artifact;

        public ArtifactDTOBuilder(
                        CommandFactory commandFactory,
                        Artifact artifact) {
                this.artifact = artifact;
                this.commandFactory = commandFactory;
        }

        public ArtifactDTO build() {
                return EntityFactory.create(ArtifactDTO::new, artifact, builder -> {
                        builder
                                        .with(dto -> dto.setId(artifact.getId()))
                                        .with(dto -> dto.setKind(artifact.getKind()))
                                        .with(dto -> dto.setProject(artifact.getProject()))
                                        .with(dto -> dto.setName(artifact.getName()))
                                        .with(dto -> dto.setSpec(ConversionUtils.reverse(
                                                        artifact.getSpec(),
                                                        commandFactory,
                                                        "cbor")))
                                        .with(
                                                        dto -> dto.setExtra(ConversionUtils.reverse(
                                                                        artifact.getExtra(),
                                                                        commandFactory,
                                                                        "cbor")))
                                        .with(dto -> dto.setState(artifact.getState() == null ? State.CREATED.name()
                                                        : artifact.getState().name()))
                                        .with(dto -> dto.setCreated(artifact.getCreated()))
                                        .with(dto -> dto.setUpdated(artifact.getUpdated()))
                                        .with(dto -> dto.setEmbedded(artifact.getEmbedded()))
                                        .with(dto -> dto.setState(artifact.getState() == null ? State.CREATED.name()
                                                        : artifact.getState().name()));

                });
        }
}