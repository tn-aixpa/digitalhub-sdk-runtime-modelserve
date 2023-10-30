package it.smartcommunitylabdhub.core.components.infrastructure.factories.runtimes;

import it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables.Runnable;
import it.smartcommunitylabdhub.core.models.base.RunStatus;
import it.smartcommunitylabdhub.core.models.entities.function.specs.FunctionBaseSpec;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.run.specs.RunBaseSpec;
import it.smartcommunitylabdhub.core.models.entities.task.specs.TaskBaseSpec;

/**
 * Runtime expose builder, run and parse method
 */
public interface Runtime {
    <F extends FunctionBaseSpec, T extends TaskBaseSpec, R extends RunBaseSpec> R build(
            F funSpec,
            T taskSpec,
            R runSpec,
            String kind
    );

    Runnable run(RunDTO runDTO);

    // TODO: parse should get and parse result job for the given runtime.
    RunStatus parse();
}
