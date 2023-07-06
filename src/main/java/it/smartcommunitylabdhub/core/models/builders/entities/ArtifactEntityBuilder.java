package it.smartcommunitylabdhub.core.models.builders.entities;

import it.smartcommunitylabdhub.core.components.fsm.enums.ArtifactState;
import it.smartcommunitylabdhub.core.models.builders.EntityFactory;
import it.smartcommunitylabdhub.core.models.converters.ConversionUtils;
import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.entities.Artifact;

public class ArtifactEntityBuilder {

        private ArtifactDTO artifactDTO;

        public ArtifactEntityBuilder(
                        ArtifactDTO artifactDTO) {
                this.artifactDTO = artifactDTO;
        }

        /**
         * Build a artifact from a artifactDTO and store extra values as a cbor
         * 
         * @return
         */
        public Artifact build() {
                Artifact artifact = EntityFactory.combine(
                                ConversionUtils.convert(artifactDTO, "artifact"), artifactDTO,
                                builder -> {
                                        builder
                                                        .with(a -> a.setExtra(
                                                                        ConversionUtils.convert(artifactDTO.getExtra(),

                                                                                        "cbor")))
                                                        .with(a -> a.setSpec(
                                                                        ConversionUtils.convert(artifactDTO.getSpec(),

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
                                                                        ? ArtifactState.CREATED
                                                                        : ArtifactState.valueOf(
                                                                                        artifactDTO.getState())))
                                                        .with(a -> a.setExtra(
                                                                        ConversionUtils.convert(artifactDTO.getExtra(),

                                                                                        "cbor")))
                                                        .with(a -> a.setSpec(
                                                                        ConversionUtils.convert(artifactDTO.getSpec(),

                                                                                        "cbor")))
                                                        .with(a -> a.setEmbedded(artifactDTO.getEmbedded()));
                                });
        }
}