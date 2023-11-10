package it.smartcommunitylabdhub.modules.nefertem.models.specs.task;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.entities.task.specs.TaskBaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "infer", entity = SpecEntity.TASK)
public class TaskInferSpec extends TaskBaseSpec<TaskInferSpec> {
    @Override
    protected void configureSpec(TaskInferSpec taskInferSpec) {
    }
}
