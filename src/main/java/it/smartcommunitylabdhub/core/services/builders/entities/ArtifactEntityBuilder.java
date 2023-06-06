package it.smartcommunitylabdhub.core.services.builders.entities;

import it.smartcommunitylabdhub.core.models.converters.CommandFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.entities.Artifact;
import it.smartcommunitylabdhub.core.models.enums.State;
import it.smartcommunitylabdhub.core.services.factory.EntityFactory;

public class ArtifactEntityBuilder {

        private CommandFactory commandFactory;
        private ArtifactDTO artifactDTO;

        public ArtifactEntityBuilder(
                        CommandFactory commandFactory,
                        ArtifactDTO artifactDTO) {
                this.artifactDTO = artifactDTO;
                this.commandFactory = commandFactory;
        }

        /**
         * Build a artifact from a artifactDTO and store extra values as a cbor
         * 
         * @return
         */
        public Artifact build() {
                Artifact artifact = EntityFactory.combine(
                                ConversionUtils.convert(artifactDTO, commandFactory, "artifact"), artifactDTO,
                                builder -> {
                                        builder
                                                        .withIf(artifactDTO.getEmbedded(), a -> a.setExtra(
                                                                        ConversionUtils.convert(artifactDTO.getExtra(),
                                                                                        commandFactory,
                                                                                        "cbor")))
                                                        .withIf(artifactDTO.getEmbedded(), a -> a.setSpec(
                                                                        ConversionUtils.convert(artifactDTO.getSpec(),
                                                                                        commandFactory,
                                                                                        "cbor")));
                                });

                return artifact;
        }

        /**
         * Update a artifact
         * TODO: x because if element is not passed it override causing empty field
         * 
         * @param artifact
         * @return
         */
        public Artifact update(Artifact artifact) {
                return EntityFactory.combine(
                                artifact, artifactDTO, builder -> {
                                        builder
                                                        .with(a -> a.setKind(artifactDTO.getKind()))
                                                        .with(a -> a.setProject(artifactDTO.getProject()))
                                                        .with(a -> a.setState(artifactDTO.getState() == null
                                                                        ? State.CREATED
                                                                        : State.valueOf(artifactDTO.getState())))
                                                        .with(a -> a.setExtra(
                                                                        ConversionUtils.convert(artifactDTO.getExtra(),
                                                                                        commandFactory,
                                                                                        "cbor")))
                                                        .with(a -> a.setSpec(
                                                                        ConversionUtils.convert(artifactDTO.getSpec(),
                                                                                        commandFactory,
                                                                                        "cbor")))
                                                        .with(a -> a.setEmbedded(artifactDTO.getEmbedded()));
                                });
        }
}