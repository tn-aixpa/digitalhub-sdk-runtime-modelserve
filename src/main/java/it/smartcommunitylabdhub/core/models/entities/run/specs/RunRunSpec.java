package it.smartcommunitylabdhub.core.models.entities.run.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.models.base.specs.BaseSpec;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "run", entity = SpecEntity.RUN)
public class RunRunSpec extends RunBaseSpec {

    @Override
    protected <S extends T,
            T extends BaseSpec> void configure(S concreteSpec) {
        super.configure(concreteSpec);

        RunRunSpec runRunSpec = (RunRunSpec) concreteSpec;
        this.setTask(runRunSpec.getTask());
        this.setTaskId(runRunSpec.getTaskId());
        this.setInputs(runRunSpec.getInputs());
        this.setOutputs(runRunSpec.getOutputs());
        this.setLocalExecution(runRunSpec.isLocalExecution());
        this.setParameters(runRunSpec.getParameters());
        this.setExtraSpecs(runRunSpec.getExtraSpecs());
        this.setInputs(runRunSpec.getInputs());

    }
}

