package it.smartcommunitylabdhub.dbt.models.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import it.smartcommunitylabdhub.core.models.entities.task.specs.TaskBaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "transform", entity = SpecEntity.TASK)
public class TaskTransformSpec extends TaskBaseSpec {

    @Override
    protected <S extends T,
            T extends BaseSpec> void configure(S concreteSpec) {

        TaskTransformSpec taskTransformSpec = (TaskTransformSpec) concreteSpec;
        this.setFunction(taskTransformSpec.getFunction());
        this.setExtraSpecs(taskTransformSpec.getExtraSpecs());
    }
}
