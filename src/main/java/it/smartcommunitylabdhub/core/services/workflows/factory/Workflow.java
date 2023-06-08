package it.smartcommunitylabdhub.core.services.workflows.factory;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.function.Function;

public class Workflow {
    private final List<Function<Object, Object>> steps;

    public Workflow(List<Function<Object, Object>> steps) {
        this.steps = steps;
    }

    /**
     * Execute step
     * 
     * @param input
     * @return
     */
    public Object execute(Object input) {
        return steps.stream()
                .reduce(Function.identity(), Function::andThen)
                .apply(input);
    }

    /**
     * Execute step async
     * 
     * @param input
     * @return
     */
    public CompletableFuture<Object> executeAsync(Object input) {
        CompletableFuture<Object> future = CompletableFuture.completedFuture(input);
        for (Function<Object, Object> step : steps) {
            future = future.thenComposeAsync(result -> CompletableFuture.supplyAsync(() -> step.apply(result)));
        }
        return future;
    }
}