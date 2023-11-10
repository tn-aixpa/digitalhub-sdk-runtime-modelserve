package it.smartcommunitylabdhub.modules.nefertem.models.specs.task;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.entities.task.specs.TaskBaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "metric", entity = SpecEntity.TASK)
public class TaskMetricSpec extends TaskBaseSpec<TaskMetricSpec> {
    @Override
    protected void configureSpec(TaskMetricSpec taskMetricSpec) {

    }
}
