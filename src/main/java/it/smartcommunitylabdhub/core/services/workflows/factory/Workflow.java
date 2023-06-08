
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
     * Execute step async every step pass the result to the next function.
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

// package it.smartcommunitylabdhub.core.services.workflows.factory;

// import java.util.List;
// import java.util.concurrent.CompletableFuture;
// import java.util.function.Function;

// public class Workflow {
// private final List<Function<Object, Object>> steps;

// public Workflow(List<Function<Object, Object>> steps) {
// this.steps = steps;
// }

// public Object execute(Object input) {
// Object result = null;
// for (Function<Object, Object> step : steps) {
// result = step.apply(result);
// }
// return result;
// }

// public CompletableFuture<Object> executeAsync(Object input) {
// CompletableFuture<Object> future = CompletableFuture.completedFuture(input);
// for (Function<Object, Object> step : steps) {
// future = future.thenApplyAsync(step);
// }
// return future;
// }
// }
