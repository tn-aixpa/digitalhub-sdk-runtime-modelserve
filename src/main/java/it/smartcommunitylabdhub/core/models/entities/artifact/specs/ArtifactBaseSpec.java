package it.smartcommunitylabdhub.core.models.entities.artifact.specs;

import com.fasterxml.jackson.annotation.JsonProperty;
import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ArtifactBaseSpec<S extends ArtifactBaseSpec<S>> extends BaseSpec<S> {
    private String key;

    @JsonProperty("src_path")
    private String srcPath;

    @JsonProperty("target_path")
    private String targetPath;

    @Override
    protected void configureSpec(S concreteSpec) {
        this.setKey(concreteSpec.getKey());
        this.setSrcPath(concreteSpec.getSrcPath());
        this.setTargetPath(concreteSpec.getTargetPath());
        this.setExtraSpecs(concreteSpec.getExtraSpecs());
    }
}
