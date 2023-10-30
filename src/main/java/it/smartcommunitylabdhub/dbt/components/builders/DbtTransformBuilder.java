package it.smartcommunitylabdhub.dbt.components.builders;

import it.smartcommunitylabdhub.core.annotations.infrastructure.BuilderComponent;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.BaseBuilder;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.Builder;
import it.smartcommunitylabdhub.core.models.entities.function.specs.FunctionBaseSpec;
import it.smartcommunitylabdhub.core.models.entities.run.specs.RunBaseSpec;
import it.smartcommunitylabdhub.core.models.entities.task.specs.TaskBaseSpec;
import it.smartcommunitylabdhub.core.utils.MapUtils;

import java.util.Map;

@BuilderComponent(runtime = "dbt", task = "transform")
public class DbtTransformBuilder extends BaseBuilder implements Builder {

    @Override
    public <F extends FunctionBaseSpec,
            T extends TaskBaseSpec,
            R extends RunBaseSpec> R build(F funSpec, T taskSpec, R runSpec) {

        // Merge spec
        Map<String, Object> extraSpecs =
                MapUtils.mergeMultipleMaps(funSpec.toMap(), taskSpec.toMap());

        // Update run specific spec
        runSpec.getExtraSpecs().putAll(extraSpecs);

        // Return a run spec
        return runSpec;
    }
}
