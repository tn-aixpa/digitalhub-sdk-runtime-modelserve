package it.smartcommunitylabdhub.core.services.workflows;

import it.smartcommunitylabdhub.core.services.workflows.factory.Workflow;

import java.util.Queue;
import java.util.concurrent.*;

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
        executorService.scheduleWithFixedDelay(this::pollWorkflows, 0, interval, TimeUnit.MILLISECONDS);
    }

    private void pollWorkflows() {
        while (!workflowQueue.isEmpty()) {
            Workflow workflow = workflowQueue.poll();
            CompletableFuture<Object> future = CompletableFuture.completedFuture(null);
            final Workflow currentWorkflow = workflow;

            future = future.thenComposeAsync(result -> currentWorkflow.executeAsync(result));
            future.join();
            workflowQueue.offer(currentWorkflow);
        }
    }

    public void stopPolling() {
        executorService.shutdown();
        try {
            if (!executorService.awaitTermination(5, TimeUnit.SECONDS)) {
                executorService.shutdownNow();
                if (!executorService.awaitTermination(5, TimeUnit.SECONDS)) {
                    System.err.println("Unable to shutdown executor service.");
                }
            }
        } catch (InterruptedException e) {
            executorService.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
