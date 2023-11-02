package it.smartcommunitylabdhub.core.models.entities.artifact.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "artifact", entity = SpecEntity.ARTIFACT)
public class ArtifactArtifactSpec extends ArtifactBaseSpec {
    @Override
    protected <S extends T, T extends BaseSpec> void configure(S concreteSpec) {
        ArtifactArtifactSpec artifactArtifactSpec = (ArtifactArtifactSpec) concreteSpec;
        this.setKey(artifactArtifactSpec.getKey());
        this.setTargetPath(artifactArtifactSpec.getTargetPath());
        this.setSrcPath(artifactArtifactSpec.getSrcPath());
        this.setExtraSpecs(artifactArtifactSpec.getExtraSpecs());
    }
}
