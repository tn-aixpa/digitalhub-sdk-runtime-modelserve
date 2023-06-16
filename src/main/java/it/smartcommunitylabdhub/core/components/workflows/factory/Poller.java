package it.smartcommunitylabdhub.core.components.workflows.factory;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class Poller implements Runnable {
    private final List<Workflow> workflowList;
    private final ScheduledExecutorService executorService;
    private final long delay;
    private final boolean reschedule;
    private final String name;

    public Poller(String name, List<Workflow> workflowList, long delay, boolean reschedule) {
        this.name = name;
        this.workflowList = workflowList;
        this.executorService = Executors.newSingleThreadScheduledExecutor();
        this.delay = delay;
        this.reschedule = reschedule;
    }

    public void startPolling() {
        System.out.println("Poller [" + name + "] start: " + Thread.currentThread().getName());
        executorService.schedule(this, delay, TimeUnit.SECONDS);
    }

    @Override
    public void run() {
        CompletableFuture<Void> allWorkflowsFuture = CompletableFuture.completedFuture(null);

        // Execute the workflows sequentially
        for (Workflow workflow : workflowList) {
            allWorkflowsFuture = allWorkflowsFuture.thenComposeAsync(result -> executeWorkflowAsync(workflow));
        }

        allWorkflowsFuture.whenComplete((result, exception) -> {
            if (exception != null) {
                // TODO: manage exception
            }

            if (reschedule) {
                System.out.println("Poller [" + name + "] reschedule: " + Thread.currentThread().getName());
                System.out.println("-------------------------------------------------------------------");

                // Delay the rescheduling to ensure all workflows have completed
                executorService.schedule(() -> startPolling(), delay, TimeUnit.SECONDS);
            }
        });
    }

    private CompletableFuture<Void> executeWorkflowAsync(Workflow workflow) {
        CompletableFuture<Void> workflowExecution = new CompletableFuture<>();

        CompletableFuture.runAsync(() -> {
            try {
                workflow.execute(null);
                workflowExecution.complete(null);
            } catch (Exception e) {
                workflowExecution.completeExceptionally(e);
            }
        });

        return workflowExecution;
    }

    public void stopPolling() {
        System.out.println("Poller [" + name + "] stop: " + Thread.currentThread().getName());
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
