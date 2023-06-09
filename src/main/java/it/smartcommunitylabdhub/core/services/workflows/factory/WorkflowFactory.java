package it.smartcommunitylabdhub.core.services.workflows.factory;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

/**
 * This is a workflow factory ... the idea is that each kind function,
 * artifact, dataitem, workflow has their workflow
 * to speak with Some external services.
 */
public class WorkflowFactory {
    private final List<Function<?, ?>> steps;

    private WorkflowFactory() {
        this.steps = new ArrayList<>();
    }

    public static WorkflowFactory builder() {
        return new WorkflowFactory();
    }

    public <I, O> WorkflowFactory step(Function<I, O> step) {
        steps.add(step);
        return this;
    }

    public <I, O> WorkflowFactory step(Function<I, O> step, I argument) {
        steps.add(input -> step.apply(argument));
        return this;
    }

    @SuppressWarnings("unchecked")
    public <I, O> WorkflowFactory step(Function<I, O> step, I... argument) {
        steps.add(input -> step.apply((I) argument));
        return this;
    }

    @SuppressWarnings("unchecked")
    public <I, O> WorkflowFactory conditionalStep(Function<I, Boolean> condition, Function<I, O> step) {
        steps.add((Function<Object, Object>) (input) -> {
            if (condition.apply((I) input)) {
                return step.apply((I) input);
            } else {
                return input; // Skip the step
            }
        });
        return this;
    }

    public Workflow build() {
        return new Workflow(steps);
    }
}
