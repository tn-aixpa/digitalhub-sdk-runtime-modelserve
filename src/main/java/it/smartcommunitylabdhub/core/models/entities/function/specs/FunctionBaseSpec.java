package it.smartcommunitylabdhub.core.models.entities.function.specs;

import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public abstract class FunctionBaseSpec extends BaseSpec {
    private String source;
}
