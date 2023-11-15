package it.smartcommunitylabdhub.modules.nefertem.components.builders;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.Builder;
import it.smartcommunitylabdhub.core.models.entities.run.specs.RunRunSpec;
import it.smartcommunitylabdhub.core.utils.MapUtils;
import it.smartcommunitylabdhub.modules.nefertem.models.specs.function.FunctionNefertemSpec;
import it.smartcommunitylabdhub.modules.nefertem.models.specs.task.TaskInferSpec;

import java.util.Map;

/**
 * NefetermInferBuilder
 * <p>
 * You can use this as a simple class or as a registered bean. If you want to retrieve this as bean from BuilderFactory
 * you have to register it using the following annotation:
 *
 * @BuilderComponent(runtime = "nefertem", task = "infer")
 */

public class NefertemInferBuilder implements Builder<
        FunctionNefertemSpec,
        TaskInferSpec,
        RunRunSpec> {

    @Override
    public RunRunSpec build(
            FunctionNefertemSpec funSpec,
            TaskInferSpec taskSpec,
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
