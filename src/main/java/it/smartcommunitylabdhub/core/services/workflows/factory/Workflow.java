
package it.smartcommunitylabdhub.core.services.workflows.factory;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.function.Function;

public class Workflow {
    private final List<Step<?, ?>> steps;

    public Workflow(List<Step<?, ?>> steps) {
        this.steps = steps;
    }

    @SuppressWarnings("unchecked")
    public <I, O> O execute(I input) {
        Object result = input;
        for (Step<?, ?> step : steps) {
            if (step instanceof ConditionalStep) {
                ConditionalStep<I, O> conditionalStep = (ConditionalStep<I, O>) step;
                if (!conditionalStep.getCondition().test(input)) {
                    continue; // Skip this step if the condition is not met
                }
            }
            result = step.execute(result);
        }
        return (O) result;
    }

    @SuppressWarnings("unchecked")
    public <I, O> CompletableFuture<O> executeAsync(I input) {
        CompletableFuture<Object> future = CompletableFuture.completedFuture(input);
        for (Step<?, ?> step : steps) {
            if (step instanceof ConditionalStep) {
                ConditionalStep<I, O> conditionalStep = (ConditionalStep<I, O>) step;
                if (!conditionalStep.getCondition().test(input)) {
                    continue; // Skip this step if the condition is not met
                }
            }
            future = future.thenComposeAsync(result -> CompletableFuture.supplyAsync(() -> step.execute(result)));
        }
        return future.thenApply(result -> (O) result);
    }
}
