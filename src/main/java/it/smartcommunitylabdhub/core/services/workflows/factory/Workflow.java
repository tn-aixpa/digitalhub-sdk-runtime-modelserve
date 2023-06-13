
package it.smartcommunitylabdhub.core.services.workflows.factory;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.function.Function;

public class Workflow {
    private final List<Function<?, ?>> steps;

    public Workflow(List<Function<?, ?>> steps) {
        this.steps = steps;
    }

    /**
     * Execute step
     *
     * @param input
     * @return
     */
    @SuppressWarnings("unchecked")
    public <I, O> O execute(I input) {
        Object result = input;
        for (Function<?, ?> step : steps) {
            result = ((Function<Object, Object>) step).apply(result);
        }
        return (O) result;
    }

    /**
     * Execute step async every step pass the result to the next function.
     *
     * @param input
     * @return
     */
    @SuppressWarnings("unchecked")
    public <I, O> CompletableFuture<O> executeAsync(I input) {
        CompletableFuture<Object> future = CompletableFuture.completedFuture(input);
        for (Function<Object, Object> step : (List<Function<Object, Object>>) (List<?>) steps) {
            future = future.thenComposeAsync(result -> CompletableFuture.supplyAsync(() -> step.apply(result)));
        }
        return future.thenApply(result -> (O) result);
    }
}