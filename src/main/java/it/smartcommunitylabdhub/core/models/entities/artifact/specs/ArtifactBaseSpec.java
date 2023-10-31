package it.smartcommunitylabdhub.core.models.entities.artifact.specs;

import com.fasterxml.jackson.annotation.JsonProperty;
import it.smartcommunitylabdhub.core.models.base.BaseSpec;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class ArtifactBaseSpec extends BaseSpec {
    private String key;

    @JsonProperty("src_path")
    private String srcPath;
    
    @JsonProperty("target_path")
    private String targetPath;
}
