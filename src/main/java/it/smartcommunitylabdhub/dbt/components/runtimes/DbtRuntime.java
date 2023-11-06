package it.smartcommunitylabdhub.dbt.components.runtimes;

import it.smartcommunitylabdhub.core.annotations.infrastructure.RuntimeComponent;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.Builder;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.builders.BuilderFactory;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runnables.Runnable;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runners.Runner;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.runners.RunnerFactory;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecEntity;
import it.smartcommunitylabdhub.core.components.infrastructure.factories.specs.SpecRegistry;
import it.smartcommunitylabdhub.core.components.infrastructure.runtimes.BaseRuntime;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunAccessor;
import it.smartcommunitylabdhub.core.models.accessors.utils.RunUtils;
import it.smartcommunitylabdhub.core.models.base.RunStatus;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import it.smartcommunitylabdhub.core.models.entities.function.specs.FunctionBaseSpec;
import it.smartcommunitylabdhub.core.models.entities.run.RunDTO;
import it.smartcommunitylabdhub.core.models.entities.run.specs.RunBaseSpec;
import it.smartcommunitylabdhub.core.models.entities.task.specs.TaskBaseSpec;
import org.springframework.beans.factory.annotation.Autowired;

@RuntimeComponent(runtime = "dbt")
public class DbtRuntime extends BaseRuntime {

    @Autowired
    SpecRegistry<? extends Spec<?>> specRegistry;

    public DbtRuntime(BuilderFactory builderFactory, RunnerFactory runnerFactory) {
        super(builderFactory, runnerFactory);
    }


    @Override
    public <F extends FunctionBaseSpec<?>,
            T extends TaskBaseSpec<?>,
            R extends RunBaseSpec<?>> R build(F funSpec, T taskSpec, R runSpec, String kind) {

        // Retrieve builder using task kind
        Builder builder = getBuilder(kind);

        // Build and return RunSpec
        return builder.build(
                funSpec,
                taskSpec,
                runSpec);
    }

    @Override
    public Runnable run(RunDTO runDTO) {

        // Retrieve base run spec to use task
        RunBaseSpec<?> runBaseSpec = (RunBaseSpec<?>) specRegistry.createSpec(
                runDTO.getKind(),
                SpecEntity.RUN,
                runDTO.getSpec()
        );
        RunAccessor runAccessor = RunUtils.parseRun(runBaseSpec.getTask());
        Runner runner = getRunner(runAccessor.getTask());
        return runner.produce(runDTO);
    }


    @Override
    public RunStatus parse() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'parse'");
    }

}
