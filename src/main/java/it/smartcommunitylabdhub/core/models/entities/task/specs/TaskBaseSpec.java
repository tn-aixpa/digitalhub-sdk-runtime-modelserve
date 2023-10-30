package it.smartcommunitylabdhub.core.models.entities.task.specs;

import it.smartcommunitylabdhub.core.models.base.BaseSpec;
import lombok.*;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Builder
public class TaskBaseSpec extends BaseSpec {
    String function;
}
