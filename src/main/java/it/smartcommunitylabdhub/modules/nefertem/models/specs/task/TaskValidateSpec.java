package it.smartcommunitylabdhub.modules.nefertem.models.specs.task;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.entities.task.specs.TaskBaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "validate", entity = SpecEntity.TASK)
public class TaskValidateSpec extends TaskBaseSpec<TaskValidateSpec> {
    @Override
    protected void configureSpec(TaskValidateSpec taskValidateSpec) {

    }
}
