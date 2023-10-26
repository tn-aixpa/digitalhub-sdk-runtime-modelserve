package it.smartcommunitylabdhub.core.models.entities.task.specs;

import it.smartcommunitylabdhub.core.models.base.BaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public abstract class TaskSpec extends BaseSpec {
    String function;
}
