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
    private final List<Function<Object, Object>> steps;

    private WorkflowFactory() {
        this.steps = new ArrayList<>();
    }

    public static WorkflowFactory builder() {
        return new WorkflowFactory();
    }

    public WorkflowFactory step(Function<Object, Object> step) {
        steps.add(step);
        return this;
    }

    public WorkflowFactory step(Function<Object, Object> step, Object argument) {
        steps.add(input -> step.apply(argument));
        return this;
    }

    public Workflow build() {
        return new Workflow(steps);
    }
}
