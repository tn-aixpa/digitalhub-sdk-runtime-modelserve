package it.smartcommunitylabdhub.dbt.models.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.entities.task.specs.TaskBaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "transform", entity = SpecEntity.TASK)
public class TaskTransformSpec extends TaskBaseSpec<TaskTransformSpec> {


    @Override
    protected void configureSpec(TaskTransformSpec taskTransformSpec) {
        super.configureSpec(taskTransformSpec);
        this.setFunction(taskTransformSpec.getFunction());
        this.setExtraSpecs(taskTransformSpec.getExtraSpecs());
    }
}
