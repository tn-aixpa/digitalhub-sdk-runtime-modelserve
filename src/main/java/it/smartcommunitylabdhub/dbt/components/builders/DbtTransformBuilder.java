package it.smartcommunitylabdhub.dbt.components.builders;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.Builder;
import it.smartcommunitylabdhub.core.models.entities.run.specs.RunRunSpec;
import it.smartcommunitylabdhub.core.utils.MapUtils;
import it.smartcommunitylabdhub.dbt.models.specs.FunctionDbtSpec;
import it.smartcommunitylabdhub.dbt.models.specs.TaskTransformSpec;

import java.util.Map;

/**
 * DbtTransformBuilder
 * <p>
 * You can use this as a simple class or as a registered bean. If you want to retrieve this as bean from BuilderFactory
 * you have to register it using the following annotation:
 *
 * @BuilderComponent(runtime = "dbt", task = "transform")
 */

public class DbtTransformBuilder implements Builder<
        FunctionDbtSpec,
        TaskTransformSpec,
        RunRunSpec> {

    @Override
    public RunRunSpec build(
            FunctionDbtSpec funSpec,
            TaskTransformSpec taskSpec,
            RunRunSpec runSpec) {

        // Merge spec
        Map<String, Object> extraSpecs = MapUtils.mergeMultipleMaps(
                funSpec.toMap(),
                taskSpec.toMap()
        );

        // Update run specific spec
        runSpec.getExtraSpecs()
                .putAll(extraSpecs);

        // Return a run spec
        return runSpec;
    }
}
