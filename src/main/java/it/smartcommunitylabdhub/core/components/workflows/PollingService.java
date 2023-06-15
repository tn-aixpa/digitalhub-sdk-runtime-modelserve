package it.smartcommunitylabdhub.core.components.workflows;

import java.util.Queue;
import java.util.concurrent.*;

import it.smartcommunitylabdhub.core.components.workflows.factory.Workflow;

public class PollingService {
    private final Queue<Workflow> workflowQueue;
    private final ScheduledExecutorService executorService;

    public PollingService() {
        this.workflowQueue = new ConcurrentLinkedQueue<>();
        this.executorService = Executors.newSingleThreadScheduledExecutor();
    }

    public void enqueueWorkflow(Workflow workflow) {
        workflowQueue.offer(workflow);
    }

    public void startPolling(long interval) {
        executorService.schedule(this::pollWorkflows, interval, TimeUnit.SECONDS);
    }

    private void pollWorkflows() {
        if (!workflowQueue.isEmpty()) {
            Workflow workflow = workflowQueue.poll();
            CompletableFuture<Object> future = workflow.executeAsync(null);
            future.whenComplete((result, exception) -> {
                if (exception != null) {
                    // TODO: manage exception
                }

                // Schedule the next workflow after a delay
                executorService.schedule(() -> enqueueWorkflow(workflow), 5, TimeUnit.SECONDS);
                pollWorkflows(); // Trigger the next iteration immediately
            });
        } else {
            // Queue is empty for this reason schedule the next workflow after a delay
            executorService.schedule(this::pollWorkflows, 5, TimeUnit.SECONDS);
        }
    }

    public void stopPolling() {
        executorService.shutdown();
        try {
            if (!executorService.awaitTermination(5, TimeUnit.SECONDS)) {
                executorService.shutdownNow();
                if (!executorService.awaitTermination(5, TimeUnit.SECONDS)) {
                    System.err.println("Unable to shutdown executor service :(");
                }
            }
        } catch (InterruptedException e) {
            executorService.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
