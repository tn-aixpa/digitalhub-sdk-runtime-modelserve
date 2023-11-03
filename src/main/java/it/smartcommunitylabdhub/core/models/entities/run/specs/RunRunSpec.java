package it.smartcommunitylabdhub.core.models.entities.run.specs;

import it.smartcommunitylabdhub.core.annotations.common.SpecType;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@SpecType(kind = "run", entity = SpecEntity.RUN)
public class RunRunSpec extends RunBaseSpec<RunRunSpec> {
    
    @Override
    protected void configureSpec(RunRunSpec runRunSpec) {
        super.configureSpec(runRunSpec);

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

