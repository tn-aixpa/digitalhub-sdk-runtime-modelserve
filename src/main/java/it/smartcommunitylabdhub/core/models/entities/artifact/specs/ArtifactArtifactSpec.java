package it.smartcommunitylabdhub.core.models.entities.artifact.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "artifact", entity = SpecEntity.ARTIFACT)
public class ArtifactArtifactSpec extends ArtifactBaseSpec<ArtifactArtifactSpec> {
    @Override
    protected void configureSpec(ArtifactArtifactSpec artifactArtifactSpec) {
        super.configureSpec(artifactArtifactSpec);
        
        this.setKey(artifactArtifactSpec.getKey());
        this.setTargetPath(artifactArtifactSpec.getTargetPath());
        this.setSrcPath(artifactArtifactSpec.getSrcPath());
        this.setExtraSpecs(artifactArtifactSpec.getExtraSpecs());
    }
}
